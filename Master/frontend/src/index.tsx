import { browserTracingIntegration, init, replayIntegration, } from '@sentry/react';
import { StrictMode, Suspense, } from 'react';
import { createRoot, } from 'react-dom/client';

import { MainApp, } from './App';
import { apply, } from './i18n';
import en from './i18n/en.json';
import { handleError, } from './utils';
import './index.css';

if (import.meta.env.VITE_APP_SENTRY_API_KEY) init({
    dsn          : import.meta.env.VITE_APP_SENTRY_API_KEY,
    integrations : [
        browserTracingIntegration(),
        replayIntegration(),
    ],
});

apply({
    language           : navigator.language.substring(0, 2),
    supportedLanguages : [
        'en',
    ],
    fallbackLanguage   : 'en',
    resources          : {
        en : {
            translation : en,
        },
    },
}).then(() => createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <Suspense fallback='Loading'>
            <MainApp />
        </Suspense>
    </StrictMode>
)).catch(handleError);
