# Low oil pressure

Primary root cause: **the lubrication circuit cannot hold differential pressure** — oil pump weak or stopped, filter plugged, oil level low, or oil foaming.  
This is a bearing-protection trip. It is not a refrigerant leak, even when a leak later steals oil.

**Evidence:** Taken from the **Trane**, **Carrier**, and **York / JCI** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf).  
**Sources:** Trane CH530 `LOW OIL PRESSURE` — pump, level, plugged filter, transducer, refrigerant migration / foam. Trane design ΔP **18–22 psid**. Carrier 19XR **228** low oil pressure — pump, level, valves, filters, foaming at start-up; **234** high bearing temperature from the same oil path. York YK: oil pump not running, wrong rotation, VSD, worn pump, blocked inlet; change filter if pump VSD exceeds **55 Hz**.

---

## 0. The Healthy State

1. **Oil is a separate loop.** A pump takes oil from the tank, through a filter and cooler, to the bearings, then back to the tank.
2. **Differential pressure is the health meter.** OEM bands: about **18–25 psid** while running (Trane 18–22; Carrier 18–25; rolling-element Carrier up to 40). That is supply minus the refrigerant pressure the oil is fighting.
3. **Level and temperature.** Sight glass in band. Sump hot enough that refrigerant is not condensed into the oil (Carrier running sump often 52–66 °C). A heater holds that when stopped.
4. **What “healthy” looks like.** Oil ΔP is in band as soon as the pre-lube pump has run. Filter is not climbing toward a high pump frequency. Bearings are not hot. The refrigerant cycle can look perfect while this loop is already dying — that is why it needs its own R2F case.

---

## 1. The Fault

**The knob.** Degrade oil-pump capacity, plug the filter, or drop oil level, and hold / ramp until ΔP leaves the OEM band.

**The chain.**

1. **ΔP falls first.** `CH-OIL-DIS-PRES` versus tank / evaporator-referenced pressure shrinks. This is the first symptom. Refrigerant temperatures can still look like yesterday.
2. **Bearings lose film.** Metal temperature starts to rise (Carrier 234). Vibration can follow. The compressor is still turning — damage is already starting.
3. **Foam branch (if the cause is refrigerant in the oil).** A sudden low suction pressure (vane slam, leak, stuck-open EXV) boils refrigerant out of the oil. Foam will not pump. ΔP collapses even if the pump motor is fine. Carrier names this at start-up; it can happen any time suction drops.
4. **Leak branch (optional later pack).** A discharge-gas leak can carry oil out. Then this fault **and** the existing leak family overlap. For a clean first case, keep charge normal and break only the oil circuit.
5. **Trip.** **Low oil pressure** (Trane, Carrier 228). York will not start, or will stop, without oil pressure. This is a **fast** protect trip compared with a 17-hour gas leak.

**Easy mix-up.** Gas leak (oil can leave with the gas). First trip of a pure leak on the current pack is **superheat / loss of charge**, not oil ΔP. This scenario’s first trip is oil. Train them as different classes or the model will wait for a refrigerant signature that never comes.
