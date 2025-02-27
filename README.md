# docchat

This is an application that lets you chat with the conent in multiple pdfs

Usecase:
- chat with all of product manuals for all the stuff you buy at home (tools, garden,  toys, electronics etc) to find out answers on how thye woork.
- This will eliminate the need (pain) in seeing your laptop, locating the pdf manual across the difffernet folders, scrolling the exact page, reading through that entire page and other related pages everytime you have a question. for example, 
       - what is the maximum fuel tank capacity of your car, what is the cutting depth of your tool, how to adjust this car seat, how do i clean this toooy 

Heree is how you run it.

1. Download the repo to yoour local laptop (you can also run in a cloud machines and access the app from browser anywhere)
2. install the python libraries as you see in 'notes.txt'
3. suupply the kekys via .env file or via command line for the following variables (Azure, AWS, Pinecone, Directory path (optional))

          AZURE_OPENAI_API_KEY=xx
          AZURE_OPENAI_ENDPOINT=xx
          AZURE_OPENAI_DEPLOYMENT_NAME=xx
          AZURE_OPENAI_EMBED_NAME=xx
          PINECONE_API_KEY=xx
          (optional) DIR_PATH=xx 
    
          aws_access_key_id = "xx"
          aws_secret_access_key = "xx"
   
5. Run mainaws.py if you have a llm access via aws bedrock or run mainaz.py if youo ahve llm access via azure cloud or change the llm calls in the main*.py as appropiate 

How to use the application 

- upload all the product manual pdfs that you may have accumulated over the years for the different products you may have bought
     - for example, user manual for your car, manual for that newly bought cutting tool
- Ask a question in the chat window, like 


High level architecture (how the program wors) 
<coming soon>
