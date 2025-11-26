import { useList, useNavigation, } from '@refinedev/core';
import { Button, Table, Tag, Typography, } from 'antd';
import { intlFormat, } from 'date-fns';
import { useTranslation, } from 'react-i18next';

import type { Device, Telemetry, } from '../data/models';
import { ResourceList, } from './ResourceList';

export const TelemetryList = () => {
    const { result : { data, }, } = useList<Device>({
        resource : 'devices',
    });

    const { show, } = useNavigation();

    const { t, } = useTranslation();

    return (
        <ResourceList<Telemetry> resource='telemetry'>
            {() => (
                <>
                    <Table.Column<Telemetry>
                        dataIndex='deviceId'
                        title={t('labels.telemetry.deviceId')}
                        render={(value : string) => {
                            const handleClick = () => show('devices', value);

                            return (
                                <Button
                                    type='link'
                                    onClick={handleClick}>
                                    {data?.find(device => device.id === value)?.displayName ?? value}
                                </Button>
                            );
                        }} />
                    <Table.Column<Telemetry>
                        width={240}
                        dataIndex='sensorType'
                        title={t('labels.telemetry.sensorType')}
                        render={(value : string) => (
                            <>
                                {value === 'temperature' && (
                                    <Tag color='green'>
                                        {t('labels.telemetry.sensorTypes.temperature')}
                                    </Tag>
                                )}
                                {value === 'humidity' && (
                                    <Tag color='blue'>
                                        {t('labels.telemetry.sensorTypes.humidity')}
                                    </Tag>
                                )}
                                {value === 'battery' && (
                                    <Tag color='orange'>
                                        {t('labels.telemetry.sensorTypes.battery')}
                                    </Tag>
                                )}
                            </>
                        )} />
                    <Table.Column<Telemetry>
                        width={80}
                        dataIndex='value'
                        title={t('labels.telemetry.value')}
                        render={value => (
                            <Typography.Text>
                                {value ? value.toFixed(1) : '-'}
                            </Typography.Text>
                        )} />
                    <Table.Column<Telemetry>
                        width={200}
                        dataIndex='timestamp'
                        title={t('labels.telemetry.timestamp')}
                        render={value => intlFormat(new Date(value), {
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
