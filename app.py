import openai
import random
import os
import json

# Initialize OpenAI API key
if "openai.api_key" not in globals():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    print("OpenAI API key initialized from environment variable.")
else:
    openai.api_key = "YOUR_API_KEY"
    print("OpenAI API key initialized from script.")

# Function to generate a prompt based on a user-defined topic
def generate_prompt(topic):
    # Use OpenAI API to generate prompts based on the topic
    prompts = openai.Completion.create(
        engine="davinci",
        prompt=f"Possible prompts related to {topic}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated prompts from the API response
    generated_prompts = [
        choice.text.strip()
        for choice in prompts.choices
        if choice.text.strip() != ""
    ]

    # If no prompts were generated, use a default prompt
    if not generated_prompts:
        prompt = "Tell me about " + topic
    else:
        # Choose a random prompt from the generated prompts
        prompt = random.choice(generated_prompts)

    return prompt

# Function to generate a ChatGPT response
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            n=1,
            stop=None,
            max_tokens=1024,
            temperature=0.7,
        )
    except openai.error.InvalidRequestError as e:
        print("Error:", e)
        return "Error: " + str(e)

    # Extract the chatbot's response from the API response
    chat_response = response.choices[0].text.strip()

    return chat_response


# Main function to generate prompts and responses
def main():
    try:
        
        # Get user input for topic, default to empty string if no topic provided
        topic = input("Enter a topic for the prompt (press Enter for a random prompt): ").strip()

        if topic:
            prompt = generate_prompt(topic)
        else:
            prompt = generate_prompt("a random topic")

        # Generate ChatGPT response based on prompt
        response = generate_response(prompt)

        # Print prompt and response
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        
        # Save prompt and response to a json file
        with open("prompt_response.json", "w") as f:
            f.write(f'{{"prompt": "{prompt}", "response": "{response}"}}')
        
    except KeyboardInterrupt:
        print("Exiting...")
        exit()

if __name__ == "__main__":
    main()
