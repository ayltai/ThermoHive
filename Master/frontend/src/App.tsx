import { ThemedLayout, useNotificationProvider, } from '@refinedev/antd';
import { type I18nProvider, Refine, } from '@refinedev/core';
import routerProvider from '@refinedev/react-router';
import { ErrorBoundary, } from '@sentry/react';
import { Alert, App, ConfigProvider, theme, Typography, } from 'antd';
import { useTranslation, } from 'react-i18next';
import { createHashRouter, Navigate, Outlet, RouterProvider, } from 'react-router';

import { dataProvider, } from './data';
import { resources, routes, } from './routes';

const RefineProvider = () => {
    const { i18n, t, } = useTranslation();

    const i18nProvider: I18nProvider = {
        changeLocale : locale => i18n.changeLanguage(locale),
        getLocale    : () => i18n.language,
        translate    : (key, options : Record<string, unknown>, defaultMessage) => defaultMessage ? t(key, defaultMessage, options) : t(key, options),
    };

    return (
        <Refine
            dataProvider={dataProvider}
            i18nProvider={i18nProvider}
            notificationProvider={useNotificationProvider}
            routerProvider={routerProvider}
            options={{
                disableTelemetry : true,
                title            : {
                    icon : (
                        <div style={{
                            marginTop : 8,
                        }}>
                            <img
                                width={24}
                                height={24}
                                alt={t('app.name')}
                                src='images/favicon-96x96.png' />
                        </div>
                    ),
                    text : (
                        <Typography.Title
                            style={{
                                marginLeft   : 8,
                                marginRight  : 8,
                                marginTop    : 16,
                                marginBottom : 8,
                            }}
                            level={4}>
                            {t('app.name')}
                        </Typography.Title>
                    ),
                },
            }}
            resources={resources.map(resource => ({
                ...resource,
                meta : {
                    ...resource.meta,
                    label : t(resource.meta.label),
                },
            }))}>
            <Outlet />
        </Refine>
    );
};

const MainLayout = () => (
    <ThemedLayout
        Header={() => null}
        Footer={() => null}>
        <Outlet />
    </ThemedLayout>
);

const router = createHashRouter([
    {
        path    : '/',
        index   : true,
        element : (
            <Navigate
                replace
                to='/devices' />
        ),
    }, {
        Component : RefineProvider,
        children  : [
            {
                Component : MainLayout,
                children  : routes,
            },
        ],
    }, {
        path    : '*',
        element : <Navigate to='/' />,
    },
]);

export const MainApp = () => (
    <ConfigProvider theme={{
        algorithm : theme.darkAlgorithm,
        token     : {
            colorPrimary : '#f57c00',
        },
    }}>
        <App>
            <ErrorBoundary fallback={<Alert.ErrorBoundary />}>
                <RouterProvider router={router} />
            </ErrorBoundary>
        </App>
    </ConfigProvider>
);
