import { CloseCircleFilled, CheckCircleFilled, } from '@ant-design/icons';
import { useNavigation, } from '@refinedev/core';
import { Button, Table, Tag, Typography, } from 'antd';
import { intlFormat, } from 'date-fns';
import { useTranslation, } from 'react-i18next';

import type { Device, } from '../data/models';
import { ResourceList, } from './ResourceList';

export const DeviceList = () => {
    const { show, } = useNavigation();

    const { t, } = useTranslation();

    return (
        <ResourceList<Device> resource='devices'>
            {() => (
                <>
                    <Table.Column<Device>
                        width={80}
                        dataIndex='lastSeen'
                        title={t('labels.device.status')}
                        align='center'
                        render={(value : string) => new Date().getTime() - new Date(value).getTime() > 24 * 60 * 60 * 1000 ? (
                            <CloseCircleFilled style={{
                                fontSize : 16,
                                color    : '#f44336',
                            }} />
                        ) : (
                            <CheckCircleFilled style={{
                                fontSize : 16,
                                color    : '#4caf50',
                            }} />
                        )} />
                    <Table.Column<Device>
                        dataIndex='displayName'
                        title={t('labels.device.displayName')}
                        render={(value, record) => {
                            const handleClick = () => show('devices', record.id);

                            return (
                                <Button
                                    size='small'
                                    type='link'
                                    onClick={handleClick}>
                                    {value ?? t('placeholders.notSet')}
                                </Button>
                            );
                        }} />
                    <Table.Column<Device>
                        width={200}
                        dataIndex='mode'
                        title={t('labels.device.mode')}
                        render={(value : string) => (
                            <>
                                {value && value.includes('actuator') && (
                                    <Tag
                                        style={{
                                            marginRight : 8,
                                        }}
                                        color='#7b1fa2'>
                                        {t('labels.device.modes.actuator')}
                                    </Tag>
                                )}
                                {value && value.includes('sensor') && (
                                    <Tag color='#0097a7'>
                                        {t('labels.device.modes.sensor')}
                                    </Tag>
                                )}
                                {!value && (
                                    <Typography.Text>
                                        {t('placeholders.notSet')}
                                    </Typography.Text>
                                )}
                            </>
                        )} />
                    <Table.Column<Device>
                        width={240}
                        dataIndex='lastSeen'
                        title={t('labels.device.lastSeen')}
                        render={(value : string) => intlFormat(value, {
                            dateStyle : 'medium',
                            timeStyle : 'medium',
                        }, {
                            locale : navigator.language,
                        })} />
                </>
            )}
        </ResourceList>
    );
};
