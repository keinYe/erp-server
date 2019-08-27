# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from sqlalchemy import func
from pycrawler.module import db, api
from pycrawler.crawler.models import (
    Brands,
    Materials,
    Price,
    Catalog
)
from flask import jsonify

post_parser = reqparse.RequestParser()
post_parser.add_argument('page', type=int)
post_parser.add_argument('brand_id', type=int)
post_parser.add_argument('brand_name', type=str)
post_parser.add_argument('catalog_id', type=int)

class MaterialApi(Resource):
    def get(self, id):
        material = db.session.query(Materials).filter(Materials.id==id).first()
        if material is not None:
            return material.to_json()
        return '', 200

class MaterialListApi(Resource):
    def get(self):
        count = db.session.query(func.count(Materials.id)).scalar()
        material = db.session.query(Materials).limit(20).offset(0)
        if material is not None:
            return jsonify({
                'total_count': count,
                'page': 0,
                'material': [x.to_json() for x in material]
            })
        return '', 200

    def post(self):
        args = post_parser.parse_args()
        count = db.session.query(func.count(Materials.id)).scalar()
        page = args.get('page')
        offset = 0
        if isinstance(page, int):
            offset = page * 20

        material = db.session.query(Materials).limit(20).offset(offset)
        if material is not None:
            return jsonify({
                'total_count': count,
                'page': page,
                'material': [x.to_json() for x in material]
            })
        return '', 200

class BrandListApi(Resource):
    def get(self):
        count = db.session.query(func.count(Brands.id)).scalar()
        brands = db.session.query(Brands).limit(20).offset(0)
        if brands is not None:
            return jsonify({
                'total_count': count,
                'page': 0,
                'brands': [x.to_json() for x in brands]
            })
        return '', 200

    def post(self):
        args = post_parser.parse_args()
        count = db.session.query(func.count(Brands.id)).scalar()
        page = args.get('page')
        offset = 0
        if isinstance(page, int):
            offset = page * 20
        brands = db.session.query(Brands).limit(20).offset(offset)
        if brands is not None:
            return jsonify({
                'total_count': count,
                'page': page,
                'brands': [x.to_json() for x in brands]
            })
        return '', 200

class BrandMaterialApi(Resource):
    def post(self):
        args = post_parser.parse_args()
        page = args.get('page')
        brand_id = args.get('brand_id')
        brand_name = args.get('brand_name')
        offset = 0
        if isinstance(page, int):
            offset = page * 20
        if brand_id is not None:
            brand = db.session.query(Brands).filter(Brands.id == brand_id).first()
        elif brand_name is not None:
            brand = db.session.query(Brands).filter(Brand.name.like('%'+brand_name+'%')).first()
        else:
            return '', 200
        count = db.session.query(Materials).filter(Materials.brand_id == brand.id).count()
        material = db.session.query(Materials).filter(Materials.brand_id == brand.id).limit(20).offset(offset)
        return jsonify({
            'total_count': count,
            'page': page,
            'brand': brand.to_json(),
            'material': [x.to_json() for x in material]
        })

class CatalogApi(Resource):
    def get(self, id):
        catalog = db.session.query(Catalog).filter(Catalog.id == id).first()
        if not catalog:
            return '', 401
        material = None
        count = 0
        if catalog.parent:
            count = db.session.query(Materials).filter(Materials.catalog_id == catalog.id).count()
            material = db.session.query(Materials).filter(Materials.catalog_id == catalog.id).limit(20).offset(0)
            # material = db.session.query(Materials).filter(Materials.brand_id == 1).limit(20).offset(0)
        return jsonify({
            'total_count': count,
            'page': 0,
            'catalog': catalog.to_json(),
            'material': [x.to_json() for x in material] if material else None
        })

class CatalogListApi(Resource):
    def post(self):
        args = post_parser.parse_args()
        page = args.get('page')
        catalog_id = args.get('catalog_id')
        catalog = db.session.query(Catalog).filter(Catalog.id == id).first()
        return '', 401
        material = None
        count = 0
        if catalog.parent:
            count = db.session.query(Materials).filter(Materials.catalog_id == catalog.id).count()
            material = db.session.query(Materials).filter(Materials.catalog_id == catalog.id).limit(20).offset(page*20)
            page = 0
        return jsonify({
            'total_count': count,
            'page': page,
            'catalog': catalog.to_json(),
            'material': [x.to_json() for x in material] if material else None
        })

api.add_resource(MaterialApi, '/api/v0.1/crawler/material/<int:id>')
api.add_resource(MaterialListApi, '/api/v0.1/crawler/materials')
api.add_resource(BrandListApi, '/api/v0.1/crawler/brands')
api.add_resource(BrandMaterialApi, '/api/v0.1/crawler/brand/material')
api.add_resource(CatalogApi, '/api/v0.1/crawler/catalog/<int:id>')
