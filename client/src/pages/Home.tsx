import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

type Aggregator = {
  id: number;
  mac_address: string;
  name: string;
};

type Device = {
  id: number;
  name: string;
  mac_address: string;
  aggregator_id: number;
};

export type Metric = {
  id: number;
  name: string;
  device_id: number;
};

const Homepage = () => {
  const navigate = useNavigate();
  const [metricId, setMetricId] = useState<number | null>(null);
  const [selectedAggregator, setSelectedAggregator] =
    useState<Aggregator | null>(null);
  const [aggregators, setAggregators] = useState<Aggregator[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [devices, setDevices] = useState<Device[]>([]);
  const [metrics, setMetrics] = useState<Metric[]>([]);
  // const [loading, setDataStale] = useState(true);

  const fetchAggregators = async () => {
    const response = await fetch(
      `${process.env.REACT_APP_API_ENDPOINT}/aggregators`
    );
    const data: Aggregator[] = await response.json();
    setAggregators(data);
  };

  const fetchDevices = async () => {
    const response = await fetch(
      `${process.env.REACT_APP_API_ENDPOINT}/devices?aggregator_id=${selectedAggregator!.id}`
    );
    console.log(response);
    const data: Device[] = await response.json();
    setDevices(data);
  };

  const fetchMetrics = async () => {
    const response = await fetch(
      `${process.env.REACT_APP_API_ENDPOINT}/metrics?device_id=${selectedDevice!.id}`
    );
    const data: Metric[] = await response.json();
    setMetrics(data);
  };

  useEffect(() => {
    fetchAggregators();
  }, []);

  useEffect(() => {
    if (selectedAggregator) {
      fetchDevices();
    }
  }, [selectedAggregator]);

  useEffect(() => {
    if (selectedDevice) {
      fetchMetrics();
    }
  }, [selectedDevice]);

  const routeToDevice = () => {
    if (!metricId) {
      alert("Please enter a device ID");
      return;
    }
    navigate("/metrics/" + metricId);
  };

  return (
    <div className="flex flex-col justify-center items-center gap-6">
      <div className="flex flex-col gap-3 items-center ">
        <h1 className="text-5xl font-bold">Welcome!</h1>
        <h2 className="text-2xl">
          Enter a metric ID or browse for a device...
        </h2>
      </div>
      <hr className="w-full h-[2px]" />
      <h2 className="text-2xl">Enter a device ID</h2>
      <div className="rounded-lg border-gray-400 w-full flex items-center justify-center">
        <input
          className="outline-none border-2 border-gray-200 focus:border-gray-200 -my-2 border-transparent rounded-l-2xl duration-200 border-2 px-4 py-2"
          placeholder="Device ID"
          onChange={(e) => setMetricId(parseInt(e.target.value))}
        />
        <button
          onClick={() => routeToDevice()}
          className="bg-black text-white font-bold border-2 border-black duration-200 hover:bg-blue-600 w-[60px] py-2 rounded-r-xl"
        >
          Go
        </button>
      </div>
      <hr className="w-full h-[2px]" />
      <h2 className="text-2xl">Browse for a device</h2>
      <div className="w-full">
        <div className="rounded-lg w-full flex items-center justify-center">
          <div className="w-full h-[30px] bg-white rounded-lg flex justify-left items-center">
            <div className="w-1/3 rounded-l-lg flex flex-col gap-2 justify-start items-center py-3 px-2">
              <h1 className="text-xl font-bold pb-4">AGGREGATOR</h1>
            </div>
            <div className="w-1/3 rounded-l-lg flex flex-col gap-2 justify-start items-center py-3 px-2">
              <h1 className="text-xl font-bold pb-4">DEVICE</h1>
            </div>
            <div className="w-1/3 rounded-l-lg flex flex-col gap-2 justify-start items-center py-3 px-2">
              <h1 className="text-xl font-bold pb-4">METRIC</h1>
            </div>
          </div>
        </div>
        <div className="rounded-lg border-gray-400 w-full flex items-center justify-center">
          <div className="w-full h-[300px] bg-white border-2 border-black rounded-lg flex justify-left items-center">
            <div className="w-1/3 h-[300px]  rounded-l-lg flex flex-col gap-2 justify-start items-center py-3 px-2">
              {aggregators.map((aggregator) =>
                aggregator === selectedAggregator ? (
                  <div className="cursor-pointer bg-black w-full h-[40px] flex items-center justify-center rounded-md">
                    <p className="select-none font-bold text-white ">
                      {aggregator.name}
                    </p>
                  </div>
                ) : (
                  <div
                    onClick={() => setSelectedAggregator(aggregator)}
                    className="cursor-pointer hover:font-bold duration-200 hover:bg-gray-300 text-black w-full h-[40px] flex items-center justify-center rounded-md"
                  >
                    <p className="select-none">{aggregator.name}</p>
                  </div>
                )
              )}
            </div>
            <hr className="h-full -mt-[3px] w-[2px] bg-black" />
            <div className="w-1/3 h-[300px]  rounded-l-lg flex flex-col gap-2 justify-start items-center py-3 px-2">
              {devices.map((device) =>
                device === selectedDevice ? (
                  <div className="cursor-pointer bg-black w-full h-[40px] flex items-center justify-center rounded-md">
                    <p className="select-none font-bold text-white ">
                      {device.name}
                    </p>
                  </div>
                ) : (
                  <div
                    onClick={() => setSelectedDevice(device)}
                    className="cursor-pointer hover:font-bold duration-200 hover:bg-gray-300 text-black w-full h-[40px] flex items-center justify-center rounded-md"
                  >
                    <p className="select-none">{device.name}</p>
                  </div>
                )
              )}
            </div>
            <hr className="h-full -mt-[3px] w-[2px] bg-black" />
            <div className="w-1/3 h-[300px]  rounded-l-lg flex flex-col gap-2 justify-start items-center py-3 px-2">
              {metrics.map((metric) => (
                <Link
                  to={`/metric/${metric.id}`}
                  className="cursor-pointer hover:font-bold duration-200 hover:bg-gray-300 text-black w-full h-[40px] flex items-center justify-center rounded-md"
                >
                  {metric.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
      <hr className="w-full h-[2px]" />
    </div>
  );
};

export default Homepage;
