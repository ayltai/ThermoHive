import { captureException, } from '@sentry/react';

export const handleError = (error : any) => {
    if (import.meta.env.PROD) {
        captureException(error);
    } else {
        console.error(error);
    }
};
