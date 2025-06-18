import React, { useMemo } from 'react';
import { Scatter } from 'react-chartjs-2';
import PropTypes from 'prop-types';
import { Chart as ChartJS, Title, Tooltip, Legend, ScatterController, LinearScale, LogarithmicScale, PointElement, LineElement } from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(
    Title,
    Tooltip,
    Legend,
    ScatterController,
    LinearScale,
    LogarithmicScale,
    PointElement,
    LineElement
);

const GenericGraph = ({ data, config }) => {
    const xScaleType = config.xScaleType || 'linear';
    const yScaleType = config.yScaleType || 'linear';
    const xAxisTitle = config.xAxisTitle || 'X Axis';
    const yAxisTitle = config.yAxisTitle || 'Y Axis';

    const chartData = useMemo(() => {
        if (!data) return null;

        return {
            datasets: Object.keys(data).map((key, index) => {
                const { label, color, pointRadius, pointHoverRadius, showLine, pointStyle } = config[key] || {};
                const randomColor = color || `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;

                return {
                    label: label || `Dataset ${index + 1}`,
                    data: data[key].map(point => ({ x: point.x, y: point.y })),
                    backgroundColor: randomColor,
                    borderColor: randomColor,
                    pointRadius: pointRadius || 2,
                    pointHoverRadius: pointHoverRadius || 8,
                    showLine: showLine !== undefined ? showLine : true,
                    borderWidth: 1,
                    pointStyle: pointStyle || 'circle',
                };
            }),
        };
    }, [data, config]);

    if (!chartData) return <p>Loading data...</p>;

    const formatLogarithmicTick = (value) => {
        if (value === 0) return '0';
        return `10^${Math.log10(value).toFixed(0)}`;
    };

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <Scatter
                data={chartData}
                options={{
                    responsive: true,
                    maintainAspectRatio: true, // Maintain aspect ratio
                    aspectRatio: 2, // Ensures x:y ratio stays constant
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return `(${context.raw.x}, ${context.raw.y})`;
                                },
                            },
                        },
                    },
                    scales: {
                        x: {
                            type: xScaleType,
                            position: 'bottom',
                            title: {
                                display: true,
                                text: xAxisTitle,
                                font: {
                                    size: 12,
                                },
                            },
                            ticks: {
                                callback: xScaleType === 'logarithmic' ? formatLogarithmicTick : undefined,
                                autoSkip: true,
                                maxTicksLimit: 10,
                            },
                        },
                        y: {
                            type: yScaleType,
                            position: 'left',
                            title: {
                                display: true,
                                text: yAxisTitle,
                                font: {
                                    size: 12,
                                },
                            },
                        },
                    },
                }}
            />
        </div>
    );
};

GenericGraph.propTypes = {
    data: PropTypes.objectOf(
        PropTypes.arrayOf(
            PropTypes.shape({
                x: PropTypes.number.isRequired,
                y: PropTypes.number.isRequired,
            })
        )
    ).isRequired,
    config: PropTypes.objectOf(
        PropTypes.shape({
            label: PropTypes.string,
            color: PropTypes.string,
            pointRadius: PropTypes.number,
            pointHoverRadius: PropTypes.number,
            showLine: PropTypes.bool,
            pointStyle: PropTypes.oneOf(['circle', 'triangle', 'rect', 'rectRot', 'cross', 'crossRot', 'star', 'line', 'dash']),
            xScaleType: PropTypes.oneOf(['linear', 'logarithmic']),
            yScaleType: PropTypes.oneOf(['linear', 'logarithmic']),
            xAxisTitle: PropTypes.string,
            yAxisTitle: PropTypes.string,
        })
    ),
};

GenericGraph.defaultProps = {
    config: {},
};

export default GenericGraph;
