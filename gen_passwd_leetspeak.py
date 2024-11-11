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

# List of suffixes to add
suffixes = [
    "`", "``", "```", "!", "!!", "!!!", "@", "@@", "@@@", "#", "##", "###", "$", "$$", "$$$", ",", ",,", ",,,",
    ".", "..", "...", "=", "==", "===", "?", "??", "???", "!@#", "!@#!@#", "#@!", "#@!#@!", "~!@#", "#@!~",
    "~!@#$", "$#@!~", "123", "123`", "123!", "123@", "123#", "123123", "123123`", "123123!", "123123@", 
    "123123#", "321", "321`", "321!", "321@", "321#", "321312", "321321`", "321321!", "321321@", "321321#",
    "456", "456`", "456!", "456@", "456#", "456456", "456456`", "456456!", "456456@", "456456#", "654", "654`",
    "654!", "654@", "654#", "654654", "654654`", "654654!", "654654@", "654654#", "789", "789`", "789!", "789@",
    "789#", "789789", "789789`", "789789!", "789789@", "789789#", "987", "987`", "987!", "987@", "987#", "987987",
    "987987`", "987987!", "987987@", "987987#", "asd", "asdasd", "qwe", "qweqwe", "zxc", "zxczxc", "ewq", "ewqewq",
    "qwerty", "ytrewq", "aaa", "aaaa", "bbb", "bbbb", "ccc", "cccc", "sss", "ssss", "ddd", "dddd", "qqq", "qqqq",
    "www", "wwww", "eee", "eeee", "1234", "12345", "123456", "1234567", "12345678", "123456789", "0123", "01234",
    "0123456", "01234567", "012345678", "0123456789", "0", "00", "000", "0000", "11", "111", "1111", "22", "222",
    "2222", "33", "333", "3333", "44", "444", "4444", "55", "555", "5555", "66", "666", "6666", "77", "777", "7777",
    "88", "888", "8888", "99", "999", "9999", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "1000", 
    "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000"
]

# Function to display how the script works
def display_how_it_works():
    print(f"""
{Fore.YELLOW}HOW THIS SCRIPT WORKS:
{Fore.GREEN}+ Generates a list of passwords (combinations.txt) based on keyword combinations and leetspeak transformations.
+ Special characters are inserted only between keywords.
+ The output includes single keywords, combinations, and leetspeak variations, and adds specific suffixes to each.

{Fore.YELLOW}WHY NO SPECIAL CHARS AT THE END?
{Fore.GREEN}+ The generated combinations.txt will be used by munge.py, which also adds the most common suffixes at the end.
{Style.RESET_ALL}
""")

# Function to return lowercase and leetspeak versions of a word
def generate_variants(word):
    variants = set()  # Use a set to avoid duplicates

    # Generate lowercase version
    base_word = word.lower()
    variants.add(base_word)

    # Generate leetspeak transformations for each character in the base word
    leetspeak_combinations = []
    for char in base_word:
        leetspeak_combinations.append(leetspeak_map.get(char, [char]))  # Get leetspeak options or the char itself

    # Create all possible leetspeak transformations
    for leetspeak_variant in itertools.product(*leetspeak_combinations):
        leetspeak_word = ''.join(leetspeak_variant)
        variants.add(leetspeak_word)

    return list(variants)  # Return as list for compatibility with itertools

# Function to filter out combinations that end with special characters
def is_valid_combination(combination):
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
    
    # Add keyword combinations with special chars only between keywords (2 to 4 length combinations)
    for length in range(2, 5):
        combinations = itertools.permutations(keywords, length)
        for combination in combinations:
            variants = [generate_variants(word) for word in combination]
            for variant_combination in itertools.product(*variants):
                variant_combination = list(variant_combination)
                
                # Special characters between keywords only
                for i in range(len(variant_combination) - 1):
                    for special_char in special_chars:
                        with_special_in_between = variant_combination[:i + 1] + [special_char] + variant_combination[i + 1:]
                        if is_valid_combination(with_special_in_between):
                            results.add(''.join(with_special_in_between))

    # Add suffixes to each combination
    final_results = set()
    for result in results:
        final_results.add(result)  # Original combination without suffix
        for suffix in suffixes:
            final_results.add(result + suffix)

    return final_results

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
