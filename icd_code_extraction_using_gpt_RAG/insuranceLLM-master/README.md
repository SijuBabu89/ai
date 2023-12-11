# insuranceLLM (under construction 🚧)
The goal of this project is to make a NLP model that can understand a doctor's clinical report and ouput the relevant ICD (Internationl Disease Classification) codes. These codes are then used by the insurance company to give the insurance money.
## Initial Thoughts
The initial and straight forward approch that came to our minds was that we train fine tune a pre trained model to do Multi-Class Classification of the ICD codes provided we have a dataset with doctor's clinical report and the coressponding ICD codes. Unfortunately, We were not provided with such a dataset. So we brainstormed a lot and came up with 2 solutions. The major issue we thought we might face is that LLMs are not trustable. 
- **NER with calculating vector scores**
  
    This implementation focused on
    - Identifying biological entities from a clinical report using bioBERT.
    - Converting them to vectors using bioBERT embeddings.
    - Calculate the similarity score of these words with the ICD data that we already extracted ( contains ICD codes and their coresspondng description ).
    - The ICD code coressponding to the highest code will be given as the output.

    But there is an obvious flaw in this method. ICD codes have their subcodes too and their descriptions are too similar due to which the similarity scores can be too similar. Thus, even if the parent code can be identified but this fails to work to distinguish between sub ICD codes.
  
- **An ICD fine-tuned model with Attention Manipulation**
  
  This method seems more promising than the previous one. The implementation for this goes as follows
    - First we fine-tune a pre trained model (bioGPT in our case) with the ICD guidelines PDF file.
      - Here we used the PeFT technique to train the model. Bascially, we added new parameters while freezing the pre trained ones.
      - This allowed the model to learn about the guidelines that ICD uses.
    - Next, we have to teach the models about the ICD codes. For that we again fine-tuned them using the ICD tabular PDF file.
      - Right now we are at this stage, We are still not sure if this is the way. :)
    - Recognize biological entities form the clinical report using bioBERT.
    - Then, we use Attention Manipulation to amplify the attention scores of the indentified words. This ensures that the model focuses on the right words and we get a higher chance of getting the right output.

 ## Future goals
 We think the above methods can be extended in order to get a more trustable model. 
 - One such way is giving the models memory. We can do that by integrating it to a vector DB. Once a prompt is made, the model can take similar vectors form the DB and then add it to the initial prompt to get more information regarding it.
 - Reinforcement Learning is something that we can use to update the weights. But this process might take time since we also need to collect the human data.
 ## Conclusion
 We are still on the experimenting phase. We will update soon once, we get something significant.

## Installation

- Fork and clone the project,  and add a upstream remote to track main repo changes
 ```
        $ git clone https://github.com/{username}/insuranceLLM.git
        $ cd insuranceLLM
        $ git remote add upstream https://github.com/Harikrishna-AL/insuranceLLM.git
```

Create a python 3 virtualenv, and activate the environment.
```bash
        $ virtualenv venv
        $ source bin/activate
        
```

⛔️After installing new packages, update the requirements.txt file⛔️
```bash
        $ pip freeze > requirements.txt
```

Install the project dependencies from `requirements.txt`
```
        $ pip install -r requirements.txt
```

## Development

- For creating new features, create new branch locally and work on it.
- After testing the feature, create a PR.
- To fetch new changes

```bash
    $ git fetch upstream
    $ git rebase upstream/master
```
