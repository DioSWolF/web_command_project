# Web Interface Of The "Personal Assistant" Program In A Box
## Purpose
This program is created as a project modular of courses GoIT stream Web7.
Before starting work, the user must register by specifying a login and password. 
The program provides creation, editing, and storage of notes, people's contacts,
files (up to 50 MB of total memory), and news viewing. Each user has access only 
to his data.

## MIT License

Copyright (c) 2023 Andrii Truba, Dmitry Tkach , Ivan Shkvyr, Musfer Adzhymambetov, Taras Breurosh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Getting Started With The "Personal Assistant"

Open the command line in the folder where the Dockerfile is located and enter 
the following commands (note that Docker Desktop must be running)

Note that before installing the program, you must write down the access 
path to the database and the secret key in the file .env
```
docker build .
```
```
docker-compose up -d --build
```
```
docker-compose exec web python manage.py makemigrations --noinput
```
```
docker-compose exec web python manage.py migrate --noinput
```
To start working with the program, in the address bar of the browser, enter the
appropriate host and port that you specified in the .env file

## Setting Environment Variables File
Before starting the installation of the program, it is necessary to create an .env file with 
the following content (an example of this file is .env.example)

* SECRET_KEY=*{Your Secret key}*
* NAME=*{The name of your database}*
* USER=*{The username used to access the database}*
* PASSWORD=*{Your password to the database}*
* HOST=*{The fully registered domain name of the host in the DNS system or the IP address
of the host in the form of four groups of decimal numbers separated by periods}*
* PORT=*{Host port to connect to}*



