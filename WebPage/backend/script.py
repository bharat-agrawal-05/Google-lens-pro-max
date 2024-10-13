import sys
import csv
import time

def generate_csv(prompt):
    filename = 'output.csv'
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['index', 'title', 'href', 'body'])
        writer.writerow([1, prompt, f'Generated link based on {prompt}', f'Generated text based on {prompt}'])
        writer.writerow([2, f'{prompt}2', f'Generated link based on {prompt}2', f'Generated text based on {prompt}2'])

    print(f'CSV file "{filename}" generated successfully')

if __name__ == '__main__':
    time.sleep(5)
    if len(sys.argv) < 2:
        print('Prompt is required')
        sys.exit(1)

    prompt = sys.argv[1]
    generate_csv(prompt)
