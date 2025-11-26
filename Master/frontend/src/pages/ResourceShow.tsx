import { EditButton, RefreshButton, Show, useForm, } from '@refinedev/antd';
import { GetOneResponse, useGo, useShow, } from '@refinedev/core';
import { Form, Space, Typography, } from 'antd';
import { type ReactNode, } from 'react';
import { useTranslation, } from 'react-i18next';

export const ResourceShow = <T extends { id? : number | string, },>({
    resource,
    children,
} : {
    resource  : string,
    mutable?  : boolean,
    children? : ({
        data,
    } : {
        data? : GetOneResponse<T>,
    }) => ReactNode,
}) => {
    const { query : { data, isLoading, }, } = useShow<T>();

    const { form, formProps, } = useForm<T>();

    const go = useGo();

    const { t, } = useTranslation();

    return (
        <Show
            isLoading={isLoading}
            headerButtons={
                <Space>
                    <RefreshButton aria-label={t('actions.refresh')} />
                    <EditButton aria-label={t('actions.edit')} />
                </Space>
            }
            headerProps={{
                onBack : () => go({
                    to   : `/${resource}`,
                    type : 'push',
                }),
            }}
            title={
                <Typography.Title
                    style={{
                        marginTop    : 0,
                        marginBottom : 0,
                    }}
                    level={4}>
                    {t(`resources.${resource}.details`)}
                </Typography.Title>
            }>
            {data?.data?.id && (
                <Form
                    {...formProps}
                    disabled
                    labelCol={{
                        span : 8,
                    }}
                    wrapperCol={{
                        span : 16,
                    }}
                    variant='filled'
                    form={form}>
                    {children?.({
                        data,
                    })}
                </Form>
            )}
        </Show>
    );
};
