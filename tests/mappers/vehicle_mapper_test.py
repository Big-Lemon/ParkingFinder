from ParkingFinder.mappers import vehicle_mapper as module


def test_mapper():

    vehicle = module.Vehicle.get_mock_object()
    params = vehicle.to_primitive()
    vehicle = module.Vehicle(params)

    model = module.Vehicles(
        plate=vehicle.plate,
        brand=vehicle.brand,
        model=vehicle.model,
        color=vehicle.color,
        year=vehicle.year,
    )

    entity = module.VehicleMapper.to_entity(model)
    assert vehicle == entity

    model = module.VehicleMapper.to_model(entity)
    assert model.plate == entity.plate
    assert model.brand == entity.brand
    assert model.model == entity.model
    assert model.color == entity.color
    assert model.year == entity.year

    record = module.VehicleMapper.to_record(vehicle)
    assert vehicle.to_primitive() == record