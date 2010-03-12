"""
Import map data.
"""
from eve_db.models import *
from importer_classes import SQLImporter

class Importer_mapUniverse(SQLImporter):
    def import_row(self, row):
        imp_obj, created = EVEUniverse.objects.get_or_create(id=row['universeID'])
        if row['universeName']:
            imp_obj.name = row['universeName']
        imp_obj.x = row['x']
        imp_obj.x_min = row['xMin']
        imp_obj.x_max = row['xMax']
        imp_obj.y = row['y']
        imp_obj.y_min = row['yMin']
        imp_obj.y_max = row['yMax']
        imp_obj.z = row['z']
        imp_obj.z_min = row['zMin']
        imp_obj.z_max = row['zMax']
        imp_obj.radius = row['radius']
        imp_obj.save()
    
class Importer_mapRegions(SQLImporter):
    DEPENDENCIES = ['chrFactions']

    def import_row(self, row):
        imp_obj, created = EVERegion.objects.get_or_create(id=row['regionID'])
        imp_obj.name = row['regionName']
        imp_obj.x = row['x']
        imp_obj.x_min = row['xMin']
        imp_obj.x_max = row['xMax']
        imp_obj.y = row['y']
        imp_obj.y_min = row['yMin']
        imp_obj.y_max = row['yMax']
        imp_obj.z = row['z']
        imp_obj.z_min = row['zMin']
        imp_obj.z_max = row['zMax']
        
        if row['factionID']:
            faction, faction_created = EVEFaction.objects.get_or_create(id=row['factionID'])
            imp_obj.faction = faction

        imp_obj.radius = row['radius']
        imp_obj.save()
        
class Importer_mapRegionJumps(SQLImporter):
    DEPENDENCIES = ['mapRegions']

    def import_row(self, row):
        from_region = EVERegion.objects.get(id=row['fromRegionID'])
        to_region = EVERegion.objects.get(id=row['toRegionID'])
        imp_obj, created = EVERegionJump.objects.get_or_create(from_region=from_region,
                                                               to_region=to_region)
        
class Importer_mapConstellations(SQLImporter):
    DEPENDENCIES = ['chrFactions', 'mapRegions']

    def import_row(self, row):
        imp_obj, created = EVEConstellation.objects.get_or_create(id=row['constellationID'])
        imp_obj.name = row['constellationName']
        imp_obj.x = row['x']
        imp_obj.x_min = row['xMin']
        imp_obj.x_max = row['xMax']
        imp_obj.y = row['y']
        imp_obj.y_min = row['yMin']
        imp_obj.y_max = row['yMax']
        imp_obj.z = row['z']
        imp_obj.z_min = row['zMin']
        imp_obj.z_max = row['zMax']
        imp_obj.radius = row['radius']

        if row['regionID']:
            region, region_created = EVERegion.objects.get_or_create(id=row['regionID'])
            imp_obj.region = region
            
        if row['factionID']:
            faction, faction_created = EVEFaction.objects.get_or_create(id=row['factionID'])
            imp_obj.faction = faction

        imp_obj.save()
        
class Importer_mapConstellationJumps(SQLImporter):
    DEPENDENCIES = ['mapRegions', 'mapConstellations']

    def import_row(self, row):
        from_constellation = EVEConstellation.objects.get(id=row['fromConstellationID'])
        from_region = EVERegion.objects.get(id=row['fromRegionID'])
        to_constellation = EVEConstellation.objects.get(id=row['toConstellationID'])
        to_region = EVERegion.objects.get(id=row['toRegionID'])
        imp_obj, created = EVEConstellationJump.objects.get_or_create(from_constellation=from_constellation,
                                                               from_region=from_region,
                                                               to_constellation=to_constellation,
                                                               to_region=to_region)
    
class Importer_mapSolarSystems(SQLImporter):
    DEPENDENCIES = ['chrFactions', 'mapRegions', 'mapConstellations',
                    'invTypes']

    def import_row(self, row):
        imp_obj, created = EVESolarSystem.objects.get_or_create(id=row['solarSystemID'])
        imp_obj.name = row['solarSystemName']
        imp_obj.x = row['x']
        imp_obj.x_min = row['xMin']
        imp_obj.x_max = row['xMax']
        imp_obj.y = row['y']
        imp_obj.y_min = row['yMin']
        imp_obj.y_max = row['yMax']
        imp_obj.z = row['z']
        imp_obj.z_min = row['zMin']
        imp_obj.z_max = row['zMax']
        imp_obj.radius = row['radius']
        imp_obj.luminosity = row['luminosity']
        imp_obj.security_level = row['security']

        if row['securityClass']:
            imp_obj.security_class = row['securityClass']
        
        if row['border'] == 1:
            imp_obj.is_border_system = True
            
        if row['fringe'] == 1:
            imp_obj.is_fringe_system = True
            
        if row['corridor'] == 1:
            imp_obj.is_corridor_system = True
            
        if row['hub'] == 1:
            imp_obj.is_hub_system = True
            
        if row['international'] == 1:
            imp_obj.is_international = True
            
        if row['regional'] == 1:
            imp_obj.has_interregional_link = True
            
        if row['constellation'] == 1:
            imp_obj.has_interconstellational_link = True

        if row['regionID']:
            region, region_created = EVERegion.objects.get_or_create(id=row['regionID'])
            imp_obj.region = region
            
        if row['constellationID']:
            constellation, constellation_created = EVEConstellation.objects.get_or_create(id=row['constellationID'])
            imp_obj.constellation = constellation
            
        if row['sunTypeID']:
            imp_obj.sun_type = EVEInventoryType.objects.get(id=row['sunTypeID'])
            
        if row['factionID']:
            faction, faction_created = EVEFaction.objects.get_or_create(id=row['factionID'])
            imp_obj.faction = faction

        imp_obj.save()
        
class Importer_mapDenormalize(SQLImporter):
    DEPENDENCIES = ['invTypes', 'invGroups', 'mapSolarSystems',
                        'mapConstellations', 'mapRegions']

    def import_row(self, row):
        mapdenorm, created = EVEMapDenormalize.objects.get_or_create(id=row['itemID'])
        mapdenorm.orbit_id = row['orbitID']
        mapdenorm.x = row['x']
        mapdenorm.y = row['y']
        mapdenorm.z = row['z']
        mapdenorm.radius = row['radius']
        mapdenorm.name = row['itemName']
        mapdenorm.security = row['security']
        mapdenorm.celestial_index = row['celestialIndex']
        mapdenorm.orbit_index = row['orbitIndex']
            
        if row['typeID']:
            mapdenorm.type = EVEInventoryType.objects.get(id=row['typeID'])
                
        if row['groupID']:
            mapdenorm.group = EVEInventoryGroup.objects.get(id=row['groupID'])
                
        if row['solarSystemID']:
            mapdenorm.solar_system = EVESolarSystem.objects.get(id=row['solarSystemID'])
                
        if row['constellationID']:
            mapdenorm.constellation = EVEConstellation.objects.get(id=row['constellationID'])
                
        if row['regionID']:
            mapdenorm.region = EVERegion.objects.get(id=row['regionID'])
            
        mapdenorm.save()