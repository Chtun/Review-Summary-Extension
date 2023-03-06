#Import OS and System Modules
import os,sys

# import json to read review contents json file
import json

# import AI and text tokenization models
import openai, spacy

# global variables - adding cwd to the system path to access variables
sys.path.insert(0, os.getcwd())
import variables


def request_summarization(review_content):
    prompt_positive = "Pros and cons about the product in the following reviews:\n"
    prompt_negative = "Pros and cons about the product in the following reviews:\n"

    adjectives = []

    count_positive = 0
    count_negative = 0
    for review in review_content['reviews']:
        if review['content'] != None:
            if review['rating'] and float(review['rating']) > 4.5:
                count_positive+=1
                prompt_positive += review['content'] + "\n"
            elif review['rating'] and float(review['rating']) < 2.5:
                prompt_negative += review['content'] + "\n"
                    
    
    # SpaCy text breakdown
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(prompt_positive)
    for index in range(len(doc)):
        if (doc[index].pos_ == "ADJ"):
            descriptive_info = doc[index].text.capitalize()
            end = False
            p = doc[index]
            while (p.head and end != True):
                if (p.dep_ == "amod" or p.dep_ == "dobj"):
                    if (p.head.lemma_ == "be"):
                        end = True
                    else:
                        descriptive_info += " " + p.head.text.capitalize()
                        p = p.head
                else:
                    end = True
            adjectives.append(descriptive_info)

    for w in doc:
        print(w.text + ":\ntag - " + w.pos_ + "\t-\t" + str(spacy.explain(w.pos_)) + "\ndep - " + w.dep_ + "\t-\t" + str(spacy.explain(w.dep_)))


    print("Adjectives:")
    print(adjectives)
    
    print("\n" + prompt_positive)
    print(prompt_negative)


    # Summarize for the positive qualities
    # completions = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt_positive,
    #     max_tokens=256,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )

    # positive_qualities = completions.choices[0].text
    positive_qualities = "Pros:\n- Comfortable\n- Lightweight\n- Good arch support\n- True to size\n- High quality\n- Stylish\n- Can be washed in a machine\n- Good price\n- Room for orthotic insoles\n- Wide fit for those with wider feet\n- Perfect fit\n- Great for any physical activity\n- Perfect for those with plantar fasciitis"

    # Summarize for the negative qualities
    # completions = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt_negative,
    #     max_tokens=256,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )

    # negative_qualities = completions.choices[0].text
    negative_qualities = "Pros:\n-Stylish\n-Good cushion\n-Good support\n-True to size\n-Good arch support\n-Breathable\n-Good quality\n\nCons:\n-Bulky\n-Heavy\n-Poor fit\n-Runs big\n-Poor shock absorption\n-No flex\n-Poor arch support\n-Uncomfortable\n-Expensive\n-Fake/counterfeit\n-Not breathable\n-Not true to size\n-No sizes available\n-Arrived damaged/dirty\n-Arrived used"

    positive_qualities_list = positive_qualities.split("\n")
    negative_qualities_list = negative_qualities.split("\n")

    print(positive_qualities_list)
    print(negative_qualities_list)

    Pros = []
    Cons = []

    # If on_pro is 1, list under 'Pros'. If on_pro is -1, list under 'Cons'.
    on_pro = 0
    # Iterate through postive qualities list
    for i in range(len(positive_qualities_list)):
        # If the value at this index is 0, skip it
        if len(positive_qualities_list[i]) <= 0:
            continue

        # Remove any extra characters
        positive_qualities_list[i] = positive_qualities_list[i].replace('-', '')
        if positive_qualities_list[i][0] == " ":
            positive_qualities_list[i] = positive_qualities_list[i][1:]
        
        # If list element is pro or con, set on_pro
        if str.lower(positive_qualities_list[i]).find("pro") >= 0:
            on_pro = 1
        elif str.lower(positive_qualities_list[i]).find("con") >= 0:
            on_pro = -1
        # Otherwise append the quality to the appropriate list
        elif on_pro == 1:
            Pros.append(positive_qualities_list[i])
        elif on_pro == -1:
            Cons.append(positive_qualities_list[i])

    # If on_pro is 1, list under 'Pros'. If on_pro is -1, list under 'Cons'.
    on_pro = 0
    # Iterate through negative qualities list
    for i in range(len(negative_qualities_list)):
        # If the value at this index is 0, skip it
        if len(negative_qualities_list[i]) <= 0:
            continue

        # Remove any extra characters
        negative_qualities_list[i] = negative_qualities_list[i].replace('-', '')
        if negative_qualities_list[i][0] == " ":
            negative_qualities_list[i] = negative_qualities_list[i][1:]

        # If list element is pro or con, set on_pro
        if str.lower(negative_qualities_list[i]).find("pro") >= 0:
            on_pro = 1
        elif str.lower(negative_qualities_list[i]).find("con") >= 0:
            on_pro = -1
        # Otherwise append the quality to the appropriate list
        elif on_pro == 1:
            Pros.append(negative_qualities_list[i])
        elif on_pro == -1:
            Cons.append(negative_qualities_list[i])


    print("Pros:\n" + str(Pros))
    print("Cons:\n" + str(Cons))



    


if __name__ == "__main__":
    openai.api_key = variables.get_api_key()

    # open review contents json file
    json_file = open(os.getcwd() + variables.get_review_contents_path())

    # return json object as a dictionary
    review_content = json.load(json_file)

    if review_content != None:
        request_summarization(review_content)
    else:
        print("review contents json file was empty")
