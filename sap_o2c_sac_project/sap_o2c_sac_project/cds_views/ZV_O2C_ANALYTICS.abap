@AbapCatalog.sqlViewName: 'ZVO2CANALYTICS'
@AbapCatalog.compiler.compareFilter: true
@AbapCatalog.preserveKey: true
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'O2C Analytics - Main View for SAC'
@Analytics.dataCategory: #CUBE
@Analytics.settings.maxProcessingEffort: #HIGH
@VDM.viewType: #CONSUMPTION

define view ZV_O2C_ANALYTICS
  as select from vbak
  inner join      vbap on  vbak.vbeln = vbap.vbeln
  left outer join likp on  vbak.vbeln = likp.vbelv
  left outer join vbrk on  vbak.vbeln = vbrk.vbelv
  left outer join kna1 on  vbak.kunnr = kna1.kunnr
{
  // ----- Key Fields -----
  key vbak.vbeln                                          as SalesOrder,
  key vbap.posnr                                          as SalesOrderItem,

  // ----- Customer -----
      vbak.kunnr                                          as CustomerID,
      kna1.name1                                          as CustomerName,
      kna1.land1                                          as Country,
      kna1.regio                                          as Region,

  // ----- Product -----
      vbap.matnr                                          as Material,
      vbap.arktx                                          as MaterialDescription,
      vbap.kwmeng                                         as OrderQuantity,
      vbap.meins                                          as UoM,

  // ----- Revenue -----
      vbap.netwr                                          as NetValue,
      vbap.kpein                                          as UnitPrice,
      vbak.waerk                                          as Currency,

  // ----- Org Data -----
      vbak.vkorg                                          as SalesOrg,
      vbak.vtweg                                          as DistributionChannel,
      vbak.spart                                          as Division,
      vbak.vkbur                                          as SalesOffice,

  // ----- Dates -----
      vbak.audat                                          as OrderDate,
      vbak.vdatu                                          as RequestedDeliveryDate,
      likp.lfdat                                          as PlannedDeliveryDate,
      likp.wadat_ist                                      as ActualGoodsIssueDate,
      vbrk.fkdat                                          as BillingDate,

  // ----- Payment -----
      vbak.zterm                                          as PaymentTerms,

  // ----- Status -----
      vbak.gbstk                                          as OverallStatus,

  // ----- Calculated: Delivery Days -----
      cast(
        ( cast( likp.wadat_ist as abap.dec(8,0) )
        - cast( vbak.audat     as abap.dec(8,0) ) )
        as abap.int4
      )                                                   as DeliveryDays,

  // ----- Calculated: On-Time Delivery Flag -----
      case
        when likp.wadat_ist <= vbak.vdatu then 'Y'
        else 'N'
      end                                                 as OnTimeDelivery,

  // ----- Calculated: Order-to-Bill Cycle Days -----
      cast(
        ( cast( vbrk.fkdat  as abap.dec(8,0) )
        - cast( vbak.audat  as abap.dec(8,0) ) )
        as abap.int4
      )                                                   as OrderToBillCycleDays
}
where vbak.auart in ( 'OR', 'ZOR', 'ZRE' )  -- Standard, Custom, Returns
  and vbak.gbstk <> 'C'                      -- Exclude fully cancelled
