import datetime
from sqlalchemy import or_, Column, Integer, String, Float, Boolean, DateTime, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

# initialize DeclarativeBase for the models
Base = declarative_base()

#id -> integer
#title -> string
#type -> string
#reference -> string
#fc_affiliate_key -> string
#created_at -> datetime
#updated_at -> datetime

class Affiliate(Base):
    __tablename__ = 'affiliates'
    id=Column(Integer, primary_key=True)
    title=Column(String)
    website_url=Column(String)
    affiliate_products = relationship("AffiliateProduct", back_populates="affiliate")
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    fc_affiliate_key = Column(String, nullable=False)
    reference = Column(String, nullable=True)
    def __repr__(self):
        return "<affiliate(id = '%s', title='%s', website='%s', fc_affiliate_key='%s'>" % \
               (self.id, self.title, self.website_url, self.fc_affiliate_key)

class AffiliateProduct(Base):
    __tablename__ = 'affiliate_products'
    id=Column(Integer, primary_key=True)
    affiliate_product_title = Column(String)
    affiliate_product_description = Column(String)
    affiliate_product_id = Column(String)
    affiliate_product_url= Column(String)
    affiliate_product_image_url = Column(String)
    affiliate_id=Column(Integer, ForeignKey('affiliates.id'))
    affiliate = relationship("Affiliate", back_populates="affiliate_products")
    in_stock=Column(Boolean)
    price=Column(Float)
    discount=Column(Float)
    weight=Column(Float)
    crawled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    def __repr__(self):
        return "<affiliateproduct(id = '%s', name=%s, price='%s', affiliate_product_id='%s'>" % \
               (self.id, self.affiliate_product_title, self.price, self.affiliate_product_id)

### Get or create object
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
