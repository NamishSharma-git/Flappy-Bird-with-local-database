# Flappy Bird Game with Player Database and Progress Tracking

A Python implementation of the classic Flappy Bird game featuring player authentication, SQL database integration, input validation, persistent score tracking, and progressively challenging gameplay.

---

## Overview

This project recreates the Flappy Bird game while extending it with software engineering concepts such as database integration, data validation, player progress tracking, and algorithm implementation.

The project focuses on both gameplay and backend functionality by combining Python, Pygame, and MySQL into a complete application.

---

## Gameplay Features

- Endless Flappy Bird gameplay
- Progressive difficulty through increasing obstacle speed
- Animated bird movement
- Collision detection
- Real-time score tracking
- Level progression
- Retry functionality
- Main menu and game-over screens

---


## Database Features

Player information is stored using a MySQL database.

The application stores:

- Player Name
- Email
- Age
- High Score
- Current Score
- Retry Count
- Highest Level Achieved

---

## Input Validation

The application validates user input before gameplay.

Validation includes:

- Name length checks
- Character validation
- Email format validation
- Numeric age validation
- Age range validation
- Empty field detection

---

## Technologies

- Python
- Pygame
- MySQL
- MySQL Connector
- SQL

---

## Algorithms

The project implements several core algorithms and programming concepts including:

- Bubble Sort for high-score organisation
- Collision Detection
- Object-Oriented Programming
- Database CRUD Operations
- Input Validation
- Event-driven Game Loop

---

## Features

- Player login system
- Persistent database storage
- High-score tracking
- Dynamic obstacle generation
- Progressive game difficulty
- Retry system
- Real-time score display
- Animated sprites
- Keyboard and mouse controls

---

## Repository Contents

- Game logic
- Player management
- Database integration
- Input validation
- Score tracking
- Game assets
- SQL queries

---

## Project Report

A detailed explanation of the system design, implementation, database structure, testing, and evaluation is available in **Project_Report.pdf**.

---

To run the project with database support, install **XAMPP** from [https://www.apachefriends.org/](https://www.apachefriends.org/), then start the **Apache** and **MySQL** services before launching the game.
