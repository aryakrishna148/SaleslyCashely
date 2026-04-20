@AbapCatalog.sqlViewName: 'ZVO2CRFM'
@AbapCatalog.compiler.compareFilter: true
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'O2C RFM Customer Segmentation View'
@Analytics.dataCategory: #DIMENSION

define view ZV_O2C_RFM
  as select from ZV_O2C_ANALYTICS
{
  CustomerID,
  CustomerName,
  Region,

  // Recency: days since last order (lower = better)
  cast(
    dats_days_between( max( OrderDate ), sy-datum )
    as abap.int4
  )                          as RecencyDays,

  // Frequency: number of distinct orders
  count( distinct SalesOrder ) as OrderFrequency,

  // Monetary: total net revenue
  sum( NetValue )              as TotalRevenue,

  // Average order value
  avg( NetValue as abap.dec(15,2) ) as AvgOrderValue
}
group by
  CustomerID,
  CustomerName,
  Region
