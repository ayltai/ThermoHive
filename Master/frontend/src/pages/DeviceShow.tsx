import { Form, Input, Tag, Typography, } from 'antd';
import { intlFormat, } from 'date-fns';
import { useTranslation, } from 'react-i18next';

import type { Device, } from '../data/models';
import { ResourceShow, } from './ResourceShow';

export const DeviceShow = () => {
    const { t, } = useTranslation();

    return (
        <ResourceShow<Device> resource='devices'>
            {({ data, }) => (
                <>
                    <Form.Item<Device>
                        name='id'
                        label={t('labels.device.id')}>
                        <Input width='100%' disabled />
                    </Form.Item>
                    <Form.Item<Device>
                        name='displayName'
                        label={t('labels.device.displayName')}>
                        <Input width='100%' />
                    </Form.Item>
                    <Form.Item<Device>
                        name='mode'
                        label={t('labels.device.mode')}>
                        {data?.data?.mode?.includes('actuator') && (
                            <Tag
                                style={{
                                    marginRight : 8,
                                }}
                                color='#7b1fa2'>
                                {t('labels.device.modes.actuator')}
                            </Tag>
                        )}
                        {data?.data?.mode?.includes('sensor') && (
                            <Tag color='#0097a7'>
                                {t('labels.device.modes.sensor')}
                            </Tag>
                        )}
                        {!data?.data?.mode && (
                            <Typography.Text>
                                {t('placeholders.notSet')}
                            </Typography.Text>
                        )}
                    </Form.Item>
                    <Form.Item<Device>
                        name='lastSeen'
                        label={t('labels.device.lastSeen')}>
                        {data?.data && (
                            <Typography.Text>
                                {intlFormat(data.data.lastSeen, {
                                    dateStyle : 'medium',
                                    timeStyle : 'medium',
                                }, {
                                    locale : navigator.language,
                                })}
                            </Typography.Text>
                        )}
                    </Form.Item>
                </>
            )}
        </ResourceShow>
    );
};
