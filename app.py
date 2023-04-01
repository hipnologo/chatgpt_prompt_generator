import openai
import random

# Initialize OpenAI API key
openai.api_key = "YOUR_API_KEY"

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
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Main function to generate prompts and responses
def main():
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

if __name__ == "__main__":
    main()
