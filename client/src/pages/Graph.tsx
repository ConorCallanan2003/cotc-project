import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { io } from "socket.io-client";
import moment from "moment";
import { Metric } from "./Home";

const data = [
  {
    name: "Page A",
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: "Page B",
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: "Page C",
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: "Page D",
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: "Page E",
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: "Page F",
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: "Page G",
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];

type Snapshot = {
  timestamp: number;
  value: number;
};

export default function MetricPage(props: any) {
  const [chartData, setChartData] = useState<Snapshot[]>([]);
  const [metricDetails, setMetricDetails] = useState<Metric>();
  const { id } = useParams();

  const fetchMetericDetails = async () => {
    const response = await fetch(
      `${process.env.REACT_APP_API_ENDPOINT}/metric/${id}`
    );
    const data = await response.json();
    setMetricDetails(data);
  };

  useEffect(() => {
    fetchMetericDetails();
    var socket = io(process.env.REACT_APP_API_ENDPOINT);
    socket.on("connect", function () {
      socket.emit("subscribe", { metric_id: id });
    });
    socket.on("initial_data", function (data) {
      setChartData(data);
    });

    socket.on("data", function (data) {
      setChartData((prev) => {
        if (prev.filter((item) => item.timestamp === data.timestamp).length > 0)
          return prev;

        return [...prev, data];
      });
    });
  }, []);

  console.log(chartData);
  return (
    <div className="h-screen w-screen flex justify-center items-center">
      <div className="w-full h-[600px] flex flex-col gap-8 justify-start items-center">
        <h1 className="text-3xl w-[1200px] text-left font-bold">
          {metricDetails?.name}
        </h1>
        <LineChart
          width={1200}
          height={550}
          data={chartData}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#d88484" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#d88484" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#82ca9d" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="timestamp"
            tickFormatter={(unixTime) => moment(unixTime).format("HH:mm:ss Do")}
            type="number"
            name="Time"
            domain={["auto", "auto"]}
          />
          <YAxis dataKey="value" name="Value" />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Line
            isAnimationActive={false}
            type="monotone"
            dataKey="value"
            stroke="#c92e0b"
            fillOpacity={1}
            fill="url(#colorUv)"
          />
        </LineChart>
      </div>
    </div>
  );
}
