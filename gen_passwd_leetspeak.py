import itertools
import colorama
from colorama import Fore, Style
import os

colorama.init(autoreset=True)

# Leetspeak mappings
leetspeak_map = {
    'a': ['a', '@'],
    'e': ['e', '3'],
    'i': ['i', '1'],
    'o': ['o', '0'],
    's': ['s', '$'],
    't': ['t', '7'],
    'g': ['g', '9']
}

# Function to display how the script works
def display_how_it_works():
    print(f"""
{Fore.YELLOW}HOW THIS SCRIPT WORKS:
{Fore.GREEN}+ Generates a list of passwords (combinations.txt) based on keyword combinations and leetspeak transformations.
+ Special characters can appear at the beginning, between keywords, and at the end if needed.
+ The output includes single keywords, combinations, and leetspeak variations with uppercase and lowercase.

{Fore.YELLOW}WHY NO SPECIAL CHARS AT THE END?
{Fore.GREEN}+ The generated combinations.txt will be used by munge.py, which also adds the most common suffixes at the end.
{Style.RESET_ALL}
""")

# Function to return lowercase, capitalized, uppercase, and leetspeak versions of a word
def generate_variants(word):
    variants = set()  # Use a set to avoid duplicates

    # Generate lowercase, uppercase, and capitalized versions
    base_variants = [word.lower(), word.capitalize(), word.upper()]
    for base_word in base_variants:
        variants.add(base_word)

        # Generate leetspeak transformations for each character in the base word
        leetspeak_combinations = []
        for char in base_word:
            leetspeak_combinations.append(leetspeak_map.get(char.lower(), [char]))  # Get leetspeak options or the char itself

        # Create all possible leetspeak transformations for each base variant
        for leetspeak_variant in itertools.product(*leetspeak_combinations):
            leetspeak_word = ''.join(leetspeak_variant)
            variants.add(leetspeak_word)

    return list(variants)  # Return as list for compatibility with itertools

# Function to filter out combinations that end with special characters
def is_valid_combination(combination):
    # Ensure that the last element is not a special character
    return combination[-1].isalnum()

# Get user input for keywords
def get_keywords():
    print(f"{Fore.CYAN}[+] Please provide the keywords, it could be a word, number, or special chars, and separate them by commas.")
    print(f"{Fore.CYAN}[+] Ex: admin, cloud, 2023, @, !")
    
    all_keywords = []
    
    while True:
        user_input = input(Fore.YELLOW + "[+] Enter your keywords: ").strip()
        
        if not user_input:
            print(Fore.RED + "[!] Please enter some keywords.")
            continue
        
        # Split the input by commas, remove extra spaces, and ensure no empty strings
        keywords = [word.strip() for word in user_input.split(',') if word.strip()]
        all_keywords.extend(keywords)
        
        # Ask if they want to add more keywords
        while True:
            more_input = input(Fore.YELLOW + "[?] Do you want to add more? [1] Yes [2] No: ").strip().lower()
            if more_input in ['no', 'n', '2']:
                return list(dict.fromkeys(all_keywords))  # Remove duplicates and return
            elif more_input in ['yes', 'y', '1']:
                break
            else:
                print(Fore.RED + "[!] Invalid input, please choose either '1' (Yes) or '2' (No).")

# Function to generate combinations based on the pattern
def generate_combinations(keywords, special_chars):
    results = set()
    
    # Add single keywords (with variants)
    for word in keywords:
        for variant in generate_variants(word):
            results.add(variant)
    
    # Add keyword combinations without special chars (2 to 4 length combinations)
    for length in range(2, 5):
        combinations = itertools.permutations(keywords, length)
        for combination in combinations:
            if is_valid_combination(combination):
                variants = [generate_variants(word) for word in combination]
                for variant_combination in itertools.product(*variants):
                    results.add(''.join(variant_combination))
    
    # Add special character combinations (at the beginning, between, and end)
    for length in range(2, 5):
        combinations = itertools.permutations(keywords, length)
        for combination in combinations:
            variants = [generate_variants(word) for word in combination]
            for variant_combination in itertools.product(*variants):
                variant_combination = list(variant_combination)
                
                # Special characters at the beginning
                for special_char in special_chars:
                    with_special_at_begin = [special_char] + variant_combination
                    results.add(''.join(with_special_at_begin))
                
                # Special characters between keywords
                for i in range(len(variant_combination) - 1):
                    for special_char in special_chars:
                        with_special_in_between = variant_combination[:i + 1] + [special_char] + variant_combination[i + 1:]
                        if is_valid_combination(with_special_in_between):
                            results.add(''.join(with_special_in_between))
                
                # Special characters at the end
                for special_char in special_chars:
                    with_special_at_end = variant_combination + [special_char]
                    results.add(''.join(with_special_at_end))

    return results

def main():
    # Display the explanation before the script runs
    display_how_it_works()
    
    # Get keywords from the user
    keywords = get_keywords()

    # Separate special characters and normal keywords
    words = [kw for kw in keywords if kw.isalnum()]  # Letters or numbers
    special_chars = [kw for kw in keywords if not kw.isalnum()]  # Special characters

    # Display the final keywords list before proceeding
    print(f"{Fore.GREEN}[+] Final list of keywords: {keywords}")
    
    # Open a file to save the combinations
    output_file = "combinations.txt"
    with open(output_file, "w") as f:
        # Generate and write combinations
        results = generate_combinations(words, special_chars)
        for result in results:
            f.write(result + '\n')

    # Print the path to the output file
    abs_path = os.path.abspath(output_file)
    print(f"{Fore.GREEN}[+] Please check file combinations.txt at {abs_path}")

if __name__ == "__main__":
    main()
