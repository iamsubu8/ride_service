# Ride Service Backend

A backend simulation of a ride-hailing platform (like Uber/Ola) built with Django. This project models a realistic ride flow, driver allocation, and fare computation using time and distance tracking. There is no frontend; all configuration and inspection is done via Django admin and API endpoints.

---

## Features

- **Ride Lifecycle:**  
  - States: `create_ride`, `driver_assigned`, `driver_at_location`, `start_ride`, `end_ride`, `cancelled`
  - Timestamps recorded for key transitions

- **Driver Allocation:**  
  - Background job periodically assigns available drivers to unassigned rides
  - Expanding search radius by 2 km every 10 seconds (up to 10 km)
  - Prevents driver abuse (no double assignment, recent rider exclusion, cancellation rules)

- **Fare Calculation:**  
  - Fare computed at `end_ride` using:
    ```
    Fare = Base Fare + (Distance × Rate Per KM) + (Duration × Rate Per Minute) + Waiting Charges
    ```
  - All rates configurable via Django admin (`PriceConfig` model)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/iamsubu8/ride_service.git
cd ride_service
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver
```

---

## Usage

### Django Admin

- Configure base rates in `PriceConfig`
- Add drivers and riders for simulation

### API Endpoints

#### 1. Create a Ride

`POST /api/create-ride/`

**Payload:**
```json
{
  "pickup_latitude": 12.9716,
  "pickup_longitude": 77.5946,
  "drop_latitude": 12.9352,
  "drop_longitude": 77.6245,
  "rider_id": 1
}
```

#### 2. Update Ride Status

`POST /api/ride-status-update/<ride_id>/`

**Payload:**
```json
{
  "status": "driver_at_location" | "start_ride" | "end_ride"
}
```

#### 3. Driver Allocation

- Runs automatically in the background (see below)

---

## Background Driver Allocation

To periodically allocate drivers to rides, run:

```bash
python manage.py allocate_drivers
```

This command will scan for unassigned rides and match them with the nearest available driver, expanding the search radius every 10 seconds.

---

## Models

- **Rider:** Rider details and location
- **Driver:** Driver details, status, and current location
- **Ride:** Ride request, status, timestamps, fare
- **PriceConfig:** Key-value store for fare rates
---

## Configuration

- Set fare rates (`base_fare`, `price_per_km`, `price_per_min`, `waiting_charge`) in Django admin under `PriceConfig`.
- Add drivers and riders via admin or shell.

---


## Notes

- No frontend is provided; use Django admin and API endpoints for all operations.
- Driver allocation logic is in `application/utils.py`.
- Fare computation is triggered only at the `end_ride` stage.

---

