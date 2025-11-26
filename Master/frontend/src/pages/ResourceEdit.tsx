import { Edit, RefreshButton, useForm, } from '@refinedev/antd';
import { Form, type FormInstance, Typography, } from 'antd';
import type { ReactNode, } from 'react';
import { useTranslation, } from 'react-i18next';

export const ResourceEdit = <T extends { id? : number | string, },>({
    resource,
    children,
} : {
    resource  : string,
    children? : ({
        form,
    } : {
        form : FormInstance,
    }) => ReactNode,
}) => {
    const { form, formProps, saveButtonProps, } = useForm<T>({
        redirect : 'show',
    });

    const { t, } = useTranslation();

    return (
        <Edit
            headerButtons={
                <RefreshButton
                    aria-label={t('actions.refresh')}
                    recordItemId={form.getFieldValue('id')} />
            }
            saveButtonProps={saveButtonProps}
            title={
                <Typography.Title
                    style={{
                        marginTop    : 0,
                        marginBottom : 0,
                    }}
                    level={4}>
                    {t(`resources.${resource}.edit`)}
                </Typography.Title>}>
            <Form
                {...formProps}
                requiredMark
                scrollToFirstError
                labelCol={{
                    span : 8,
                }}
                wrapperCol={{
                    span : 16,
                }}
                form={form}>
                {children?.({
                    form,
                })}
            </Form>
        </Edit>
    );
};
