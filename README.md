# Gas Prices Data Source Definition (RECOPE)

## Data Source Description
This data source provides real-time and historical information regarding fuel prices in Costa Rica. It includes current rates for different types of fuel such as Super, Regular (Plus 91), and Diesel, distributed across various gas stations and bulk terminals.

## Data Provider
RECOPE (Refinadora Costarricense de Petróleo) - Open Data Portal.

## Access Method
REST API HTTP GET (CKAN API v3)

## Example Request
https://recope.go.cr

## Data Fields
- **id**: Internal record identifier.
- **Nombre del producto**: Type of fuel (e.g., Gasolina Super, Diesel).
- **Precio Total**: The final consumer price in Colones (₡).
- **Resolución**: The official ARESEP resolution document number.
- **Fecha de vigencia**: The date when the current price started being effective.

## Update Frequency
Data is updated according to ARESEP's official price changes (typically monthly or bi-weekly), reflecting the most current legal rates in the country.

## Data Format
JSON

## Potential Use Cases
- **Economic Analysis**: Tracking inflation and its correlation with fuel price fluctuations in Costa Rica.
- **Personal Budgeting Apps**: Tools that help citizens calculate monthly fuel expenses based on real-time prices.
- **Logistics & Fleet Management**: Optimization of operational costs for transport companies based on current fuel rates.
- **Public Policy Monitoring**: Analyzing the transparency and impact of price changes on the local economy.
