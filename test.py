import requests
from bs4 import BeautifulSoup


URL = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"


def main():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text("\n", strip=True)

    # Get content after the headers
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    try:
        start = lines.index("y-coordinate") + 1
    except ValueError:
        raise ValueError("Could not find 'y-coordinate'")

    data = lines[start:]

    # Each record consists of:
    # x-coordinate
    # Character
    # y-coordinate
    points = []

    for i in range(0, len(data) - 2, 3):
        x = int(data[i])
        character = data[i + 1]
        y = int(data[i + 2])

        points.append((x, y, character))

    print(points)

    # Determine grid size
    max_x = max(x for x, y, char in points)
    max_y = max(y for x, y, char in points)

    # Create grid
    grid = [[" " for _ in range(max_x + 1)]
            for _ in range(max_y + 1)]

    # Put characters at [x, y]
    for x, y, character in points:
        grid[y][x] = character

    # Print the grid
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    main()