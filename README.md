# AI Email Generator for Clients 🤖

## Introduction

This project was originally a take home assignment for an AI company. Writing personalized sales emails is a core feature. This prototype draws company data from Y Combinator, and only works with companies that are on Y Combinator (for now).

## Technologies Used

### Frontend:

- Next.js (React framework)
- Zustand (State management)
- Typescript
- TailwindCSS

### Backend:

- FastAPI
- Langchain
- OpenAI API
- Beautiful Soup
- Python

## How It Works

The Python/FastAPI server is mapped into to Next.js app under `/api/`.

This is implemented using [`next.config.js` rewrites](https://github.com/digitros/nextjs-fastapi/blob/main/next.config.js) to map any request to `/api/:path*` to the FastAPI API, which is hosted in the `/api` folder.

On localhost, the rewrite will be made to the `127.0.0.1:8000` port, which is where the FastAPI server is running.

In production, the FastAPI server is hosted as [Python serverless functions](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python) on Vercel.

## Demo

https://nextjs-fastapi-starter.vercel.app/

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn
# or
pnpm install
# AND
npm run fastapi-install
```

In `/api`, create a `.env` file and follow the `.env.example` file's format to add an OpenAI API key.

Then, this command starts both the frontend and backend servers:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The FastApi server will be running on [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Serverless Deployment

I already spent a significant amount of time on this assignment, and additionally conducted research on how I would deploy this to a serverless environment if I were to do so. Since time constraints limited me from building out the pipelines, this section is _what_ I would do for serverless deployment.

### Technologies to Use

- AWS CodeBuild
- AWS CodePipeline
- Amazon API Gateway
- AWS Lambda
- Vercel or another hosting service
- Github
- AWS Secrets Manager
- AWS CloudWatch

### Steps

- Add OpenAI API Key to AWS Secrets Manager
- Configure AWS CodePipeline
  - Create a new CodePipeline, connect it to this Git repository as a source
  - Add a build stage with CodeBuild as the provider.
  - Add a deploy stage that would send the build artifacts to where I'm hosting the site (In my case probably Vercel since it's free and compatible with Next.js)
- Deploy frontend and backend to AWS Lambda and Amazon API Gateway
  - Set up an AWS Lambda function to host the Next.js frontend, and another for the FastAPI backend "get email" endpoint
  - Create API Gateway endpoints to trigger the Lambda functions
  - Configure API Gateway to route requests to the appropriate Lambda functions based on the request paths.
- Test that the pipeline works by pushing a change to the Github repository
- Monitor application logs with CloudWatch

## What Else I Would Add

- AWS S3 buckets for file upload on the front end, with sanitization on AWS to ensure that it's a csv file.
- A toast when the email data is copied on the frontend to verify that it was copied to clipboard.
- Social media posts for LinkedIn
- For the generated data on the frontend, the ability for the user to edit the data in the rows, and checkmarks for each row for the user to select which rows they want to have emailed out (and a backend route to dispatch the emails).
- Currently my app only gets data about companies from Y Combinator, so I would add the ability to draw data about a company from different sources and then compile that data to draw information from. If no data could be found, on the backend I would either return nothing for the email message, or some kind of default email message with a generic sales email.
- A database (like Pinecone) for storing data about the user's contacts and data that has already been generated.
