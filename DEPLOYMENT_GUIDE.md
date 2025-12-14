# Deployment Guide for AI-Native Textbook Website

This guide explains how to deploy your Docusaurus website with the AI chatbot functionality.

## Architecture Overview

Your application consists of two main components:
1. **Frontend**: Docusaurus static site with chatbot widget (JavaScript/React)
2. **Backend**: FastAPI server with RAG (Retrieval-Augmented Generation) capabilities

## Deployment Prerequisites

- GitHub account (for version control)
- Backend hosting account (Railway, Heroku, Render, etc.)
- Frontend hosting account (Vercel, Netlify, GitHub Pages, etc.)

## Option 1: Deploy with Docker Compose (Recommended for consistency)

This approach deploys both frontend and backend together using Docker Compose:

1. **Ensure Docker setup is correct**
   - The Dockerfile should be configured to build the Docusaurus site from the `website` directory
   - The nginx configuration should proxy API requests to the backend

2. **Deploy with Docker Compose**
   ```bash
   # From the root directory of your project
   docker-compose up -d
   ```

3. **Access your application**
   - Frontend will be available at http://localhost:80
   - Backend API will be available at http://localhost:8000
   - The chatbot will work seamlessly as API requests are proxied to the backend

4. **Deploy to cloud platforms supporting Docker**
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - Railway (supports Docker)
   - Render (supports Docker)

## Option 2: Separate Deployment (Recommended for scalability)

### Step 1: Deploy the Backend API

#### Option A: Deploy to Railway (Recommended)

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with your GitHub account

2. **Install Railway CLI (optional)**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

3. **Deploy the backend**
   - Navigate to the `backend` directory
   - Connect your GitHub repository to Railway
   - Or use the CLI:
     ```bash
     cd backend
     railway init
     railway link
     railway up
     ```

4. **Get the backend URL**
   - After deployment, Railway will provide a URL like `https://your-app-name.up.railway.app`
   - Note this URL as you'll need it for frontend configuration

#### Option B: Deploy to Render

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create a new Web Service**
   - Connect to your GitHub repository
   - Choose the `backend` directory
   - Set environment: Python
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn src.api.main:app --host=0.0.0.0 --port=$PORT`

3. **Get the backend URL**
   - After deployment, Render will provide a URL
   - Note this URL as you'll need it for frontend configuration

### Step 2: Configure Frontend for Production

Before deploying the frontend, you need to update the ChatWidget to point to your production backend:

1. **Update the ChatWidget API URL**
   Open `website/src/components/ChatWidget/ChatWidget.jsx` and modify the fetch call:

   ```jsx
   const handleSend = async (e) => {
     e.preventDefault();
     if (!inputValue.trim() || isLoading) return;

     // Add user message
     const userMessage = {
       id: Date.now(),
       text: inputValue,
       sender: 'user',
       timestamp: new Date()
     };

     setMessages(prev => [...prev, userMessage]);
     setInputValue('');
     setIsLoading(true);
     setError(null);

     try {
       // Call the backend RAG API with your production URL
       const BACKEND_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.onrender.com'; // Replace with your actual backend URL
       const response = await fetch(`${BACKEND_URL}/api/rag/query`, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({
           textbook_id: 'main-textbook', // You may want to make this configurable
           question: inputValue
         })
       });

       if (!response.ok) {
         throw new Error(`API request failed with status ${response.status}`);
       }

       const data = await response.json();

       const botMessage = {
         id: Date.now() + 1,
         text: data.answer,
         sender: 'bot',
         timestamp: new Date()
       };

       setMessages(prev => [...prev, botMessage]);
     } catch (err) {
       console.error('Error calling chatbot API:', err);
       const errorMessage = {
         id: Date.now() + 1,
         text: 'Sorry, I encountered an error processing your question. Please try again.',
         sender: 'bot',
         timestamp: new Date()
       };
       setMessages(prev => [...prev, errorMessage]);
     } finally {
       setIsLoading(false);
     }
   };
   ```

2. **Alternative: Use environment variables**
   Create a `.env.production` file in the `website` directory:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```

### Step 3: Deploy the Frontend

#### Option A: Deploy to Vercel (Recommended)

1. **Sign up for Vercel**
   - Go to https://vercel.com
   - Sign up with your GitHub account

2. **Deploy the website**
   - Navigate to the `website` directory
   - Install dependencies: `npm install`
   - Build the site: `npm run build`
   - Connect your GitHub repository to Vercel
   - Set the root directory to `website`
   - Set build command: `npm run build`
   - Set output directory: `build`

3. **Add environment variables in Vercel dashboard**
   - Go to your project settings
   - Add environment variable: `REACT_APP_API_URL` with your backend URL

#### Option B: Deploy to Netlify

1. **Sign up for Netlify**
   - Go to https://netlify.com
   - Sign up with your GitHub account

2. **Deploy the website**
   - Connect your GitHub repository to Netlify
   - Set build command: `npm run build`
   - Set publish directory: `build`
   - Set root directory: `website`

3. **Add environment variables in Netlify dashboard**
   - Go to your site settings
   - Go to "Build & deploy" → "Environment"
   - Add variable: `REACT_APP_API_URL` with your backend URL

#### Option C: Deploy to GitHub Pages

1. **Update docusaurus.config.js**
   ```js
   const config = {
     // ...
     url: 'https://your-username.github.io', // Your GitHub domain
     baseUrl: '/your-repo-name/', // Your repository name
     // ...
   };
   ```

2. **Deploy**
   ```bash
   cd website
   npm run deploy
   ```

## Step 4: Test the Deployment

1. **Access your frontend URL** (e.g., https://your-site.vercel.app)
2. **Open the chatbot widget**
3. **Ask a question about Physical AI or Humanoid Robotics**
4. **Verify that the chatbot responds with relevant information**

## Step 5: Configure Custom Domain (Optional)

Both Vercel and Netlify allow you to add custom domains:
- Vercel: Go to project settings → Domains → Add domain
- Netlify: Go to Domain settings → Add custom domain

## Troubleshooting

### Common Issues:

1. **CORS errors**: Make sure your backend allows requests from your frontend domain
2. **API not responding**: Verify that your backend URL is correct in the frontend
3. **Build failures**: Check that all dependencies are properly listed in package.json

### Backend CORS Configuration:

If you encounter CORS issues, update your backend's CORS settings in `backend/src/api/main.py`:

```python
# In the create_app function, update CORS middleware:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],  # Replace with your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Maintenance

- Monitor both frontend and backend for performance
- Keep dependencies updated
- Consider adding analytics to track chatbot usage
- Regularly backup your content and data

## Scaling Considerations

- For high traffic, consider using a proper vector database (Pinecone, Weaviate) instead of in-memory storage
- Add caching layers for frequently asked questions
- Consider using a CDN for static assets