import React, { Component } from 'react'

export default class Glossary extends Component {

    constructor(props) {
        super(props);
        this.glossary = {
                methane_mixing_ratio_bias_corrected_mean: {
                    desc: "Column averaged dry air mixing ratio of methane",
                    unit: 'ppb',
                    unitDesc: 'Parts per Billion'
                },

                reading_count : {
                    desc: "This is the number of methane readings from a particular zone that were averaged together to obtain a final daily methane reading for the zone.",
                    unit: '',
                    unitDesc: ''
                },
                air_pressure_at_mean_sea_level_mean: {
                    desc: "This parameter is the pressure (force per unit area) of the atmosphere adjusted to the height of mean sea level. It is a measure of the weight that all the air in a column vertically above the area of Earth's surface would have at that point, if the point were located at the mean sea level.",
                    unit: 'Pa',
                    unitDesc: 'Pascals'
                },
                eastward_wind_at_100_metres_mean: {
                    desc: "This parameter is the eastward component of the 100 m wind. It is the horizontal speed of air moving towards the east, at a height of 100 metres above the surface of the Earth",
                    unit: 'm/s',
                    unitDesc: 'Meters per Second'
                }, 
                northward_wind_at_100_metres_mean: {
                    desc: "This parameter is the northward component of the 100 m wind. It is the horizontal speed of air moving towards the north, at a height of 100 metres above the surface of the Earth",
                    unit: 'm/s',
                    unitDesc: 'Meters per Second'
                },
                air_temperature_at_2_metres_mean: {
                    desc: "This parameter is the temperature of air at 2m above the surface of land, sea or inland waters.",
                    unit: 'K',
                    unitDesc: 'Kelvin'
                },
                surface_air_pressure_mean: {
                    desc: "This parameter is the pressure (force per unit area) of the atmosphere on the surface of land, sea and in-land water. It is a measure of the weight of all the air in a column vertically above the area of the Earth's surface represented at a fixed point.",
                    unit: 'Pa',
                    unitDesc: 'Pascals'
                },
                integral_wrt_time_of_surface_direct_downwelling_shortwave_flux_in_air_1hour_Accumulation_mean: {
                    desc: "This parameter is the amount of solar radiation (also known as shortwave radiation) that reaches a horizontal plane at the surface of the Earth. This parameter comprises both direct and diffuse solar radiation. It is the mean accumulation over a 1 hour period.",
                    unit: '(J/m2)',
                    unitDesc: 'Joules per square meter'
                },
                precipitation_amount_1hour_Accumulation_mean: {
                    desc: "This parameter is the accumulated liquid and frozen water, comprising rain and snow, that falls to the Earth's surface. It is the mean accumulation over a 1 hour period.",
                    unit: 'm',
                    unitDesc: 'Meters'
                },
                dew_point_temperature_at_2_metres_mean: {
                    desc: "This parameter is the temperature to which the air, at 2 metres above the surface of the Earth, would have to be cooled for saturation to occur. It is a measure of the humidity of the air.",
                    unit: 'K',
                    unitDesc: 'Kelvin'
                },
        }
    }
    render() {

        let {selectedOptionTime, selectedOptionBar} = this.props
            
        let timeKey = selectedOptionTime.value;
        let barKey = selectedOptionBar.value;

        return (
            <div>
                <h5>Glossary</h5>
                <div className="content">
                    <b>{selectedOptionBar.label}</b>
                    <ul>
                        <li><b>{this.glossary[barKey].unit}</b> - {this.glossary[barKey].unitDesc}</li>
                        <li>{this.glossary[barKey].desc}</li>
                    </ul>
                </div>
                <br/>
                {
                    (selectedOptionBar.label != selectedOptionTime.label) ? 
                        <div className="content">
                        <b>{selectedOptionTime.label}</b>
                        <ul>
                            <li><b>{this.glossary[timeKey].unit}</b> - {this.glossary[timeKey].unitDesc}</li>
                            <li>{this.glossary[timeKey].desc}</li>
                        </ul>
                    </div>
                    :
                    <div/>
                }
            </div>
        )
    }
}
