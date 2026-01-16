Social Media Web Application

A full-stack social media web application built using Django and Python, designed to allow users to connect, share content, and communicate with each other in real time. The project focuses on combining RESTful APIs with asynchronous, real-time features to simulate core functionalities of a modern social media platform.

🚀 Features
👤 User & Profile Management

User registration, login, and logout

Create and manage user profiles

Follow / Unfollow other users

📝 Blog Management

Create, Read, Update, and Delete (CRUD) blog posts

Like / Unlike blog posts

Blogs linked to user profiles

💬 Real-Time Chat

One-to-one (individual) chat

Group chat rooms

Real-time messaging using WebSockets

Asynchronous handling with Django Channels

Redis used as the channel layer for scalability

🌐 REST APIs

RESTful APIs built using Django REST Framework

APIs for users, profiles, blogs, likes, and follows

JSON-based communication between frontend and backend

🛠 Tech Stack
Backend

Django

Django REST Framework

Django Channels (Async support)

Realtime & Caching

WebSockets

Redis

Frontend

HTML

CSS

JavaScript

Database

SQLite (development)

PostgreSQL (production-ready support via Django ORM)

🧠 Architecture Highlights

Modular Django app structure for better maintainability

Separation of concerns between views, serializers, and models

Asynchronous backend for real-time communication

Scalable chat system using Redis + Channels

Secure authentication and authorization flows

🎯 Project Goals

Understand full-stack web development using Django

Implement real-time features using async programming

Design clean and scalable REST APIs

Gain hands-on experience with Redis and WebSockets

📌 Use Cases

Social networking platforms

Blog-based community applications

Real-time chat enabled web apps
