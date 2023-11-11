# Vidyo Assigment
# Video Processing Backend
This project is an assignment given by Vidyo.ai as the part of the hiring process for a student internship.
It is a backend project created using Django. This project mainly focuses on creating two APIs namely, watermark and extract_audio.

## Installation
### A step-by-step series of examples that tell you how to get a development environment running:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
   
`cd path_to_project`

3. Install the required Python packages.

`pip install -r requirements.txt`

4. Run migrations to set up the database.

`python manage.py migrate`

5. Create a superuser in order to manage the databases
   
`python manage.py createsuperuser`

6. Start the development server.

`python manage.py runserver`

### Using/Testing the Service

#### To Watermark a video:

Navigate to `http://localhost:8000/watermark/` in your web browser.
Fill out the form with the required information:
Video file to be watermarked.
Watermark image.
Position for the watermark.
Optionally:
You can also include the size and padding of the watermark

Submit the video and you'll get the respective URL of the watermarked video file.

#### To Extract Audio from a video:
Navigate to `http://localhost:8000/extract_audio/` in your web browser.
Fill out the form with the required information:

#### Checking the Database
Navigate to `http://localhost:8000/admin/` in your web browser.
Login using the username and password set while creating superuser
You can check the databases containing the metadata of both Extracted Audios and Watermarked Videos.
Video file to be extracted audio from.

Submit the video and you'll get the respective URL of the audio file.

## Containerization

### Prerequisites
Before proceeding, ensure that you have Docker installed on your system. You can download and install Docker from Docker's official website.

### Building the Docker Image
To build the Docker image of the application, navigate to the root directory of the project where the Dockerfile is located and run the following command:

`docker build -t video-watermarking-service .`
<br>
<br>
This command will build a Docker image named video-watermarking-service based on the instructions in your Dockerfile.

### Running the Docker Container
After building the image, you can run the application inside a container using the following command:

`docker run -d -p 8000:8000 --name video-watermarking-app video-watermarking-service`
<br>
<br>
This command will start a container named video-watermarking-app using the video-watermarking-service image. It will also map port 8000 of the container to port 8000 on your host machine, allowing you to access the application through http://localhost:8000.

## Architecture Explanation
![alt text](https://github.com/Jrap-bit/vidyo-processing-assignment/blob/9c6f5a5d4aa7932a4fc6fafc731326fdab2d29df/media/Architecture.jpg)

The diagram attached above shows the full architecture of how a video processing service which I designed would work. 

First a user would interact with the UI which would allow them to upload the videos they want to process along with customization options on the UI. 

The UI would then call upon the respective API endpoint with all the information entered by the user along with the video uploaded by them

The API Endpoint would now check with the Internal Queue System if there are any tasks in the queue. They would place the new task in the queue as well. This would reduce the load on the processing backend system and would allow for faster work on the existing tasks through better utilization of the available resources. 

The Load Balancer checks for the resources available on the nodes working on the backend and completing all the processing work. Once enough resources are available, it would take a task from the queue and give the task to the respective node to complete it. This ensures all nodes are working equally and no node is overburdened.

Finally after processing, we would store the data into a database. For the large videos which we need to provide to the user, we would require a BLOB (Binary Large Objects) storage system such as Amazon S3 in order to efficiently store the large number of files and allow the user to access them via a URL. The metadata of the large files would be relatively small and can be easily stored in a relational database as it would be highly structured and RDBMS would allow for easy access of the given data.

Lastly the URL from the BLOB storage is provided to the API endpoint which replies to the user so the user can access their document.

For the efficient utilization of the resources in this architecture, we can use several different methods and tools:

- **Caching:** For frequent access of data by the user, we can set up caches directly between API and the database for faster retrieval of information. Cache would mean less queries made to the database and would ensure faster delivery time for the user as well. We can implement MemCached or Redis for caching.-
-  ****Asynchronous Processing:**** We can implement asynchronous processing using Redis as a message broker so that when a user sends a request and the API endpoint places it in the task queue, it can instantly reply to the user with a loading or working-on-it message so that the user has an idea that their process is still under process. 
- **Resource Optimization:** Nodes performing the backend video processing tasks can be optimized by the use of methods such as containerization using docker or kubernetes so that the utilization of the total available resources on the system is efficient. 
- **Horizontal Scaling:** The architecture allows for horizontal scaling, i.e., one can add several nodes in parallel to the already working nodes so that we can increase the processing power of the whole system without compromising with the uptime of the system. With a container orchestration tool such as Kubernetes, one can easily add or remove nodes on the platform as well as maintain the uptime of each nodes and keep the number of nodes available on the system stable and easy to manage.
- **Database Indexing:** Database indexing is also one thing we can perform in order to speed up the search and data retrieval operations from the database.



