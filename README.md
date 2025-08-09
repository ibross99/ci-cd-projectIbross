# Liverpool Player Stats Application

This is a Python Flask application that displays the goals and assists of Liverpool players from last season. The application is containerized using Docker and has a CI/CD pipeline set up with GitHub Actions.

## Features

*   View a list of Liverpool players.
*   Click on a player to view their detailed stats (goals and assists).
*   Responsive design that works on desktop and mobile browsers.

## How to Deploy and Access

### Prerequisites

*   Docker installed on your local machine.
*   A GitHub account.

### Building and Running the Docker Container Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/<your-username>/<your-repository-name>.git
    cd <your-repository-name>
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t liverpool-player-stats .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 liverpool-player-stats
    ```

4.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5000`. You will see a list of Liverpool players. Click on a player's name to view their stats.

### CI/CD Pipeline

The CI/CD pipeline is configured using GitHub Actions and is defined in the `.github/workflows/cicd.yml` file. The pipeline is triggered on every push to the `main` branch and performs the following steps:

1.  **Linting:** The code is first checked for style and quality issues using `flake8`.
2.  **Testing:** The unit tests are run to ensure that the application is working correctly.
3.  **Building the Docker image:** If the linting and tests pass, the Docker image is built.
4.  **Security Scan:** The Docker image is scanned for vulnerabilities using Trivy.
5.  **Pushing the Docker image to GitHub Container Registry:** After a successful build and scan, the Docker image is tagged and pushed to the GitHub Container Registry.

This automated pipeline ensures that a new version of the application's container image is built and published whenever changes are pushed to the `main` branch, but only if all the quality and security checks pass.