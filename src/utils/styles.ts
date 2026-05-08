import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const branding = {
  colors: {
    bgPrimary: '#0B0F19',
    bgSecondary: '#111827',
    cardBg: '#1A2235',
    border: '#2A354F',
    primary: '#3B82F6',
    secondary: '#8B5CF6',
    textPrimary: '#F9FAFB',
    textSecondary: '#9CA3AF',
    success: '#10B981',
  },
  borderRadius: '2px',
};

export const gradients = {
  logo: 'linear-gradient(135deg, #3B82F6, #8B5CF6)',
};
