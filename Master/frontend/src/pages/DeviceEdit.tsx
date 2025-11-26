import { Form, Input, Select, } from 'antd';
import { useTranslation, } from 'react-i18next';

import type { Device, } from '../data/models';
import { ResourceEdit, } from './ResourceEdit';

export const DeviceEdit = () => {
    const { t, } = useTranslation();

    return (
        <ResourceEdit<Device> resource='devices'>
            {() => (
                <>
                    <Form.Item<Device>
                        name='displayName'
                        label={t('labels.device.displayName')}>
                        <Input width='100%' />
                    </Form.Item>
                    <Form.Item<Device>
                        name='mode'
                        label={t('labels.device.mode')}
                        normalize={value => Array.isArray(value) ? value.filter(item => item && item.length > 0).join(',') : value}
                        getValueProps={value => ({
                            value : typeof value === 'string' ? value.split(',').filter(item => item && item.length > 0) : value,
                        })}>
                        <Select
                            style={{
                                width : 200,
                            }}
                            mode='multiple'
                            options={(t('labels.device.modes', {
                                returnObjects : true,
                            }) as string[]).map(value => ({
                                label : `${value[0].toUpperCase()}${value.substring(1).toLowerCase()}`,
                                value : value.toLowerCase(),
                            }))} />
                    </Form.Item>
                </>
            )}
        </ResourceEdit>
    );
};
