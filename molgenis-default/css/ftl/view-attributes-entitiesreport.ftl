<#assign package="none"/>
<#assign entity="none"/>
<#list datasetRepository?sort_by("entity") as att>
<#if entity!= att.entity.label>
</ul>
<#if package!= att.entity.package.label>
<#assign package=att.entity.package.label/>
<h1>Package:${att.entity.package.label}</h1>
Description:
<p><#if att.entity.package.description??>${att.entity.package.description}<#else>Not provided</#if></p>

<img src="http://yuml.me/diagram/plain/class/<@compress single-line=true>
<#assign entity_in_package="none"/>
<#list datasetRepository?sort_by("entity") as att2>
<#if att2.entity.package.label == att.entity.package.label>
<#if att2.entity.extends?? && entity_in_package!= att2.entity.label>
<#assign entity_in_package=att2.entity.label/>
[${att2.entity.extends.label}]^-[${att2.entity.label}],
</#if>
<#if att2.refEntityType??>
[${att2.entity.label}]-${att2.getString("name")}(<#if att2.nillable>0..</#if><#if att2.getString("type")?contains("mref")>*<#else>1</#if>)>[${att2.refEntityType.label}],
</#if></#if>
</#list></@compress>"/>
</#if>
<h2>Table: ${att.entity.label}<#if att.entity.extends??><i><small> extends ${att.entity.extends.label}</small></i></#if></h2>
Decription:
<p><#if att.entity.description??>${att.entity.description}<#else>Not provided</#if></p>
Attributes:
<ul>
<#assign entity=att.entity.label/>
</#if>
  <li><b>${att.getString("name")}</b> (${att.getString("type")}<#if att.nillable> nillable</#if><#if att.unique> unique</#if>)<#if att.description??><br/><i>&nbsp;&nbsp;&nbsp;&nbsp;${att.getString("description")}</i></#if></li>
</#list>
