import { type DataProvider, } from '@refinedev/core';

import { API_ENDPOINT, } from '../constants';
import { camelCaseToSnakeCase, snakeCaseToCamelCase, } from '../utils/strings';

export const dataProvider : DataProvider = {
    getApiUrl : () => API_ENDPOINT,
    getList   : async ({ resource, pagination, }) => {
        const query = new URLSearchParams();

        if (pagination && pagination.mode !== 'client' && pagination.mode !== 'off') {
            if (pagination.pageSize) {
                query.append('limit', pagination.pageSize.toString());
                if (pagination.currentPage) query.append('offset', ((pagination.currentPage - 1) * pagination.pageSize).toString());
            }
        }

        const response = await fetch(`${API_ENDPOINT}/${resource}${resource === 'devices' ? '/all' : ''}${query.size ? `?${camelCaseToSnakeCase(query.toString())}` : ''}`);

        if (response.ok) {
            const data = await response.json();

            return {
                data  : data.filter((item : any) => item.id !== '544553545f4445564943455f31323334').map((item : any) => snakeCaseToCamelCase(item)),
                total : parseInt(response.headers.get('X-Total-Count') ?? data.length, 10),
            };
        }

        throw response;
    },
    // @ts-ignore
    getOne    : async ({ resource, id, }) => {
        const response = await fetch(`${API_ENDPOINT}/${resource}/${id}`);

        if (response.ok) return {
            data : snakeCaseToCamelCase(await response.json()),
        };

        throw response;
    },
    create    : async () => {
        throw new Error('Not implemented');
    },
    // @ts-ignore
    update    : async ({ resource, id, variables, meta, }) => {
        const response = await fetch(`${API_ENDPOINT}/${resource}/${id}`, {
            method  : meta?.method ?? 'PUT',
            headers : {
                'Content-Type' : 'application/json',
                ...(meta?.headers ?? {}),
            },
            // @ts-ignore
            body    : JSON.stringify(camelCaseToSnakeCase(variables)),
        });

        if (response.ok) return {
            data : snakeCaseToCamelCase(await response.json()),
        };

        throw response;
    },
    // @ts-ignore
    deleteOne : async ({ resource, id, meta, }) => {
        const response = await fetch(`${API_ENDPOINT}/${resource}/${id}`, {
            method : meta?.method ?? 'DELETE',
        });

        if (response.ok) return {
            data : snakeCaseToCamelCase(await response.json()),
        };

        throw response;
    },
};
