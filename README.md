# Purview Lineage Builder

A modern web application for building and managing data lineage in Microsoft Purview. This application allows users to:

- Search and select SQL tables and Power BI datasets
- Create lineage relationships between assets
- Manage Purview connection settings

## Features

- Modern, Apple-esque user interface
- Real-time asset search
- Secure settings management
- Direct lineage injection without overwriting existing metadata

## Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Microsoft Purview account with appropriate permissions
- Service Principal credentials for Purview authentication

## Setup

1. Clone the repository
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the backend directory with your Purview credentials:
   ```
   PURVIEW_ACCOUNT_NAME=your_account_name
   PURVIEW_CLIENT_ID=your_client_id
   PURVIEW_TENANT_ID=your_tenant_id
   PURVIEW_CLIENT_SECRET=your_client_secret
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## Usage

1. Click the settings icon in the top-right corner to configure your Purview connection details
2. Use the search boxes to find SQL tables and Power BI datasets
3. Select assets from both sides to create a lineage relationship
4. Click "Create Lineage" to establish the connection

## Deployment

This application can be deployed to Vercel:

1. Push your code to a Git repository
2. Connect the repository to Vercel
3. Configure the following environment variables in Vercel:
   - `PURVIEW_ACCOUNT_NAME`
   - `PURVIEW_CLIENT_ID`
   - `PURVIEW_TENANT_ID`
   - `PURVIEW_CLIENT_SECRET`

## Security Notes

- Never commit your `.env` file or client secrets to version control
- Use environment variables for sensitive configuration
- Consider implementing proper authentication for the web application in production

## License

MIT 