# footy-chippy

Chippy, your favourite football graph generator!
(**Ch**art (ip) **Py**thon)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
- [Conclusion](#conclusion)

## About

Welcome to Footy-Chippy, also known as Chippy, your personal football visualizer bot. Chippy is designed to scrape football data from FBref and present it in a user-friendly manner.

My two biggest passions are football and programming, and I've always enjoyed creating graphs in order to compare footballers. However, it was getting tiring pulling data from FBref and exporting excel sheets. In order to make the process more efficient, I've created a simple bot to help me automate the graphs.

Sometimes when you are comparing players, it's hard to argue against just "G/A", and people are not often ready to listen to the npxG+xA/90 statistics you throw at them. What's easy to understand and hard to refuse? A bar chart. This program will help you generate accurate and easy-to-read graphs within seconds to help bias fans better understand your point of view! Never be fooled by a midfielder on paper and a striker on the pitch.

## Features

There are 8 different statistics you can use to compare the players:

1. Standard
2. Shooting
3. Final Ball
4. Goal and Shot Creation
5. Playmaking
6. Possession
7. Pass Types
8. Passing Distance

Each graph uses its own format in order to best visualize the data.

## Getting Started

1. Clone this repository to your local machine:

<pre>
git clone https://github.com/zuhayrhasan/footy-chippy.git
cd footy-chippy
</pre>

2. Install the required packages.

<pre>
pip install -r requirements.txt
</pre>

3. Run the Chippy program:

<pre>
python chippy.py
</pre>

4. Follow the steps in order to generate your graphs!

5. Cached data:

Once statistics are generated, they are saved under:

<pre>
C:\Users\youruser\soccerdata\data\FBref  
</pre>

This is to speed up the process if repeat graphs for the same players are generated.

## Conclusion

I hope you enjoy using this program! The FBref scrapper is from this link:

https://github.com/probberechts/soccerdata

Unfortunately, there are no good free API's for advanced statistics, and I found FBref to be the best website to get the data from. This project is not for monetary use, but just a passion project which allows me to visualize statistics in a quick manner.
