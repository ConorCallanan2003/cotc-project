# Context of the Code Project
A System-Monitoring Tool that Provides Cloud Dashboards for PC and IOT Device Status and History
- Multiple IOT devices
- 2 metrics per device
  - e.g. # Running Threads, # Open Processes, CPU Temp, etc.
  - Should be values that change frequently but not at sub-second frequency
- Gather information from > 1 device locally on an agent (e.g. laptop)
- Report information to a cloud-based server
- Store a history of the data on the server
- Present a dashboard UI
- Stretch Goal: Send a message back to the device (e.g. reboot)

### Non-Functional Requirements
- Understand "the why" behind every interface and component built
- Have a flexible data flow so new devices and metrics can be added over time without massive rework
- No magical thinking, understand every line of code in detail
- Gain deeper understanding of operating systems, networks, cloud APIs, databases and other layers we depend on


### Initial Architecture Diagram
<img width="1842" alt="CotC Project Architecture Diagram" src="https://github.com/user-attachments/assets/b98618e1-b08d-4edc-a285-80f890e001a0">
