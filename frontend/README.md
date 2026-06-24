# AI Study Companion - Frontend

Modern Next.js 15 frontend for the AI Study Companion application.

## Tech Stack

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality React components
- **React Hook Form**: Form validation
- **Zod**: Schema validation
- **TanStack Query**: Data fetching and caching
- **Axios**: HTTP client

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── login/           # Login page
│   │   ├── register/        # Registration page
│   │   ├── dashboard/       # Dashboard page
│   │   ├── profile/         # Profile page
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page (redirects)
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   └── dropdown-menu.tsx
│   │   ├── layout/          # Layout components
│   │   │   ├── dashboard-header.tsx
│   │   │   └── protected-route.tsx
│   │   └── providers.tsx    # App providers
│   ├── contexts/
│   │   └── auth.context.tsx # Authentication context
│   └── lib/
│       ├── services/
│       │   └── auth.service.ts  # Auth API calls
│       ├── api.ts           # Axios instance
│       ├── types.ts         # TypeScript types
│       └── utils.ts         # Utility functions
├── public/                  # Static files
├── .env.local.example       # Environment variables template
├── next.config.js           # Next.js configuration
├── tailwind.config.ts       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
├── package.json             # Dependencies
└── README.md                # This file
```

## Setup Instructions

### Prerequisites

- Node.js 18+ 
- npm or yarn or pnpm
- Backend API running on http://localhost:8000

### Installation

1. **Navigate to frontend directory:**

```bash
cd frontend
```

2. **Install dependencies:**

```bash
npm install
```

Or with yarn:
```bash
yarn install
```

Or with pnpm:
```bash
pnpm install
```

3. **Configure environment:**

Copy `.env.local.example` to `.env.local`:

```bash
copy .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

For production, update the API URL to your deployed backend.

### Running the Development Server

```bash
npm run dev
```

Or:
```bash
yarn dev
```

Or:
```bash
pnpm dev
```

The application will be available at:
- http://localhost:3000

### Building for Production

```bash
npm run build
npm start
```

Or:
```bash
yarn build
yarn start
```

## Features Implemented (Phase 1)

### Authentication
- ✅ User registration with validation
- ✅ User login with JWT authentication
- ✅ Protected routes
- ✅ Auto-redirect on authentication
- ✅ Token storage and management
- ✅ Logout functionality

### Dashboard
- ✅ Responsive header with profile dropdown
- ✅ Social Studies subject card
- ✅ Modern card-based design
- ✅ Mobile-first responsive layout
- ✅ Clean gradient backgrounds

### Profile Management
- ✅ View profile information
- ✅ Edit full name
- ✅ Display account creation date
- ✅ Email (read-only)
- ✅ Account statistics overview

### UI/UX
- ✅ Educational theme with blue/indigo colors
- ✅ Smooth animations and transitions
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Loading states
- ✅ Error handling and display
- ✅ Success messages
- ✅ Form validation with helpful errors

## Page Routes

| Route | Description | Auth Required |
|-------|-------------|---------------|
| `/` | Home (redirects to login) | No |
| `/login` | Login page | No |
| `/register` | Registration page | No |
| `/dashboard` | Main dashboard | Yes |
| `/profile` | User profile settings | Yes |

## API Integration

All API calls go through the axios instance configured in `src/lib/api.ts`:

- Automatic JWT token injection
- 401 error handling (auto-logout)
- Standard error responses
- Base URL configuration

### API Services

Authentication service (`src/lib/services/auth.service.ts`):
- `register(data)` - Register new user
- `login(data)` - Login user
- `getCurrentUser()` - Get current user data
- `updateProfile(data)` - Update user profile
- `logout()` - Clear auth data
- `isAuthenticated()` - Check auth status

## State Management

- **Authentication**: React Context (`AuthContext`)
- **Server State**: TanStack Query
- **Form State**: React Hook Form

## Form Validation

All forms use Zod schemas with React Hook Form:

- Email validation
- Password minimum 8 characters
- Password confirmation matching
- Required fields
- Custom error messages

## Styling

Using Tailwind CSS with custom theme:

### Colors
- **Primary**: Blue (#3B82F6)
- **Accent**: Indigo (#6366F1)
- **Background**: Gradient from blue to indigo
- **Cards**: White with soft shadows

### Components
- Built with shadcn/ui
- Customizable via `tailwind.config.ts`
- Accessible and keyboard-friendly

## Deployment

### Vercel (Recommended)

1. Connect your GitHub repository
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL=https://your-backend-api.com/api/v1`
3. Deploy!

### Manual Deployment

```bash
npm run build
npm start
```

Set the `PORT` environment variable if needed.

## Development Tips

### Adding New Pages

1. Create page in `src/app/[route]/page.tsx`
2. Wrap with `<ProtectedRoute>` if auth required
3. Add route to table above

### Adding New Components

1. UI components go in `src/components/ui/`
2. Layout components in `src/components/layout/`
3. Feature components in relevant feature folders

### Adding New API Calls

1. Define types in `src/lib/types.ts`
2. Create service in `src/lib/services/`
3. Use in components with error handling

## Future Enhancements (Phase 2+)

- Study planner interface
- Examination generation UI
- AI tutor chat interface
- Progress tracking dashboard
- Analytics and insights
- Real-time notifications
- Dark mode support

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use a different port
npm run dev -- -p 3001
```

### API Connection Issues

- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure backend is running
- Check browser console for CORS errors
- Verify network requests in DevTools

### Build Errors

```bash
# Clear cache and rebuild
rm -rf .next
npm run build
```

## License

Proprietary - AI Study Companion
