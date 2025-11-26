import { List, useTable, } from '@refinedev/antd';
import { type CrudSort, type GetListResponse, type HttpError, type useTableProps, } from '@refinedev/core';
import { Table, Typography, } from 'antd';
import { type ReactNode, } from 'react';
import { useTranslation, } from 'react-i18next';

export const ResourceList = <T extends { id? : number | string, },>({
    resource,
    title,
    extraHeaders,
    filterProps,
    sorterProps,
    children,
} : {
    resource      : string,
    title?        : string,
    extraHeaders? : ({
        data,
    } : {
        data? : GetListResponse<T>,
    }) => ReactNode,
    filterProps?  : useTableProps<T, HttpError, T>['filters'],
    sorterProps?  : useTableProps<T, HttpError, T>['sorters'],
    children?     : ({
        isLoading,
        isSuccess,
        sorters,
        data,
    } : {
        isLoading? : boolean,
        isSuccess? : boolean,
        sorters    : CrudSort[],
        data?      : GetListResponse<T>,
    }) => ReactNode,
}) => {
    const { sorters, tableQuery : { data, isLoading, isSuccess, }, tableProps, } = useTable<T>({
        filters          : filterProps,
        sorters          : sorterProps,
        syncWithLocation : true,
    });

    const { t, } = useTranslation();

    return (
        <List
            title={
                <Typography.Title
                    style={{
                        marginTop    : 0,
                        marginBottom : 0,
                    }}
                    level={4}>
                    {t(title ?? `resources.${resource}`)}
                </Typography.Title>}>
            {extraHeaders?.({
                data,
            })}
            <Table
                {...tableProps}
                size='middle'
                rowKey='id'
                pagination={{
                    ...tableProps.pagination,
                    hideOnSinglePage : true,
                    showSizeChanger  : true,
                }}>
                {children?.({
                    sorters,
                    data,
                    isLoading,
                    isSuccess,
                })}
            </Table>
        </List>
    );
};
