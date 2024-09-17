# Energy harvesting threshold measurements 📈

Initial access for end charging will unfortunately have to be achieved by generating distributed non-coherent signals. To prevent all signals from destructively interfering at a particular location, multiple CSPs will generate signals at slightly different frequencies.

Multiple signals with slightly different frequencies will interfere with each other. In general, this results in a multi-tone signal with multiple frequency peaks distinguishable in the spectrum. In the time domain, this corresponds to a changing amplitude of the considered carrier wave, also known as an OFDM signal.

The harvester will not be able to convert smaller signals into energy since the energy RF harvester comes with a certain threshold voltage or minimum input power.

The goal is to investigate whether we can measure this with the MSO64B scope and get an approximation of the harvester threshold voltage.

💡UPDATE (experiment 02) ❗❗ Because the harvester input impedance is not a perfect 50 ohms, some of the power will be reflected. This power will also be forwarded to the scope via the RF splitter, leading to incorrect measurement results.❗❗ Solution, the RF circulator can deflect the reflected power from the harvester to a third port where a 50 ohm termination ensures that this power is absorbed.

🧾RF circulator datasheet [TH2528XS-X/900-928MHz](https://cdn.globalso.com/rftyt/9.2-TH2528XS（700-5000MHz.pdf)

## Measurement procedure

* 1️⃣: Sample CH1 and CH2 with MSO64B scope
* 2️⃣: Measure and define threshold level (when is NXP harvester actually charging the buffer)
* 3️⃣: Postprossing --> look when voltage of energy buffer is rising CH2 relayed to time domain measurement of CH1

![setup](https://github.com/techtile-by-dramco/cla-paper-measurements/blob/main/04-energy-harvester-signals/measurement-setup.drawio.png)

❗❗ Measure reflected power with scope to estimate S11 and reflection coefficient ❗❗

## 💬 REMARKS - Questions 💬:
* Probe has an impedance of 10 MOhm 
* How to generate the multi-tone signal?
	* 1️⃣ To START --> One usrp transmitting a multi-tone signal (MADE by Gilles)
		* Write script to capture signals from scope
		* Write postprocessing scripts
	* 2️⃣ IN THE END --> Measure with 917 MHz antenna in the Techtile construction 
		* Picking up all USRP RF carriers of all USRPs
