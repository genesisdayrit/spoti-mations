# Spotimations

## Spotify Half-Year Playlist Generator 

## About

Spotify has been around since 2006 and many listeners have now been on the platform for more than 10 years.

I whipped up this half-year-playlist-generator because I thought it would be cool to catalog all my music I've saved in Spotify into half-years to more easily revisit music I was listening to in different periods of my life.

###  The Spotify Half-Year Playlist Generator does two main things:
1. **Creates a playlist for every half-year** you've been active on Spotify, up to the current date.
2. **Populates these playlists** with songs from your saved library, placing each track in the half-year playlist corresponding to when you added it to your Liked/Saved library on Spotify.

## Getting Started

To use this script, you'll need to perform a few setup steps. This guide will walk you through obtaining your Spotify API credentials, setting up a Python virtual environment, installing dependencies, and running the script.

### Prerequisites
- Python 3.6+
- A Spotify account
- Spotify Developer credentials (Client ID and Client Secret)

### Installation
1. **Clone the repository**

```sh
git clone https://github.com/genesisdayrit/spotimations.git
cd spotimations
```

2. **Set up a virtual environment (optional but recommended)**

```sh copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install the required Python packages**

``` sh copy code
pip install -r requirements.txt
```

## **Obtain Spotify API Credentials**
1. Go to the Spotify Developer Dashboard.
2. Log in with your Spotify account.
3. Click "Create an App" and follow the prompts to create your application.
4. Once created, you'll find your Client ID and Client Secret on the app's dashboard.
5. Set up a Redirect URI in the app settings (e.g., http://localhost:8888/callback). This URI is where Spotify will redirect to after successful authentication.
6. Follow the instructions below to setup your .env file

### **Configure Your .env File**

Copy the `.env.example` file to a new file named `.env`, and fill in your Spotify credentials and chosen Redirect URI:
```
SPOTIFY_CLIENT_ID=[your_client_id_here]
SPOTIFY_CLIENT_SECRET=[your_client_secret_here]
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## **Running the Script** 
With the setup complete, you're ready to run the script and generate your half-year playlists:

```
python generate_half_year_playlists.py
```

When using a new scope for your Spotify Client-ID for the first time, you'll be prompted to authorize access to your Spotify account via an OAuth flow:
- A web browser will automatically open, directing you to log in to Spotify and authorize the application.
- This process grants the script the necessary permissions to access your Spotify data and create playlists on your behalf.

---
### Sharing Your Playlists
If you like your new playlists and would like to share them, feel free to tag me on X @_genesisdayrit, I would love to hear about them!

### Contributing
Any further contributions welcome! Instructions on forking the project are below.

#### Forking the Project
- Create your Feature Branch (git checkout -b feature/YourFeature)
- Commit your Changes (git commit -m 'Add YourFeature')
- Push to the Branch (git push origin feature/YourFeature)
- Open a Pull Request
