<#if entity.get('biobank')??>
    <#assign biobank=entity.get('biobank')>
    <#assign country=biobank.get('country')>
    <#assign contact=biobank.get('contact')>
    <#assign networks=biobank.get('network')>
</#if>

<#function printcontacts contacts>
    <#assign output>
        <#if contact.get('first_name')?? || contact.get('last_name')??>
            <tr>
                <th scope="row">Name</th>
                <td>${contact.get('first_name')!} ${contact.get('last_name')!}</td>
            </tr>
        </#if>
        <#if contact.get('email')??>
            <tr>
                <th scope="row">e-Mail</th>
                <td>${contact.get('email')}</td>
            </tr>
        </#if>
        <#if contact.get('address')?? || contact.get('zip')?? || contact.get('city')??>
            <tr>
                <th scope="row">Address</th>
                <td>
                    ${contact.get('address')!}<br/>
                    ${contact.get('zip')!} <br/>
                    ${contact.get('city'!)} <br/>
                    ${contact.get('country').get('name')!}
                </td>
            </tr>
        </#if>
        <#if contact.get('phone')??>
            <tr>
                <th scope="row">Phone</t>
                <td>${contact.get('phone')}<br></td>
            </tr>
        </#if>
    </#assign>
    <#return output>
</#function>

<#function getcontact ent>
    <#local contact = printcontacts(ent.get('contact'))>
        <#local prio = ent.get('contact_priority')>
            <#return {prio, contact}>
</#function>

<#function biobankcontact>
    <#if biobank??>

        <#local result = getcontact(biobank)>

            <#if biobank.get('network')??>
                <#list biobank.get('network') as network>
                    <#local result = getcontact(network) + result>
                </#list>
            </#if>
    </#if>

    <#local prio = 0>
        <#list result?keys as p>
            <#if p?number gt prio>
                <#local prio = p?number>
            </#if>
        </#list>
        <#local key = "" + prio>
            <#return result[key]>
</#function>

<#function collectioncontact>

    <#local result = getcontact(entity)>

        <#if entity.get('network')??>
            <#list entity.get('network') as network>
                <#local result = getcontact(network) + result>
            </#list>
        </#if>

        <#if biobank??>

            <#local result = getcontact(biobank) + result>

                <#if biobank.get('network')??>
                    <#list biobank.get('network') as network>
                        <#local result = getcontact(network) + result>
                    </#list>
                </#if>
        </#if>

        <#local prio = 0>
            <#list result?keys as p>
                <#if p?number gt prio>
                    <#local prio = p?number>
                </#if>
            </#list>
            <#local key = "" + prio>
                <#return result[key]>
</#function>
<div class="modal-content">
    <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <#if entity.get('biobank')??>
            <h2 class="modal-title">${biobank.get('name')}</h2>
            <small><strong>ID</strong>: ${biobank.get('id')}</small>
        </#if>
    </div>

    <div class="modal-body">
        <!-- Biobank details -->
        <#if entity.get('biobank')??>
            <div class="row">
                <div class="col-md-12">
                    <!-- Image and description -->
                    <div class="media">
                        <div class="media-left">
                            <a href="#">
                                <img alt="logo" width="100px"
                                     src="http://www.geonames.org/flags/x/${country.get('id')?lower_case}.gif">
                            </a>
                        </div>
                        <div class="media-body">
                            <#if biobank.get('description')??>
                                <p class="lead"><h4>${biobank.get('description')}</h4></p>
                            </#if>
                        </div>
                    </div>
                    <hr></hr>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <h4>Overview</h4>
                    <table class="table table-striped ">
                        <tbody>
                        <tr>
                            <th scope="row">Head</th>
                            <td>
                                <#if biobank.get('head_firstname')??>
                                    ${biobank.get('head_firstname')}
                                </#if>
                                <#if biobank.get('head_lastname')??>
                                    ${biobank.get('head_lastname')}
                                </#if>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Institution</th>
                            <td>
                                ${biobank.get('juridical_person')}
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">BBMRI-ERIC Partner Charter Signed</th>
                            <td>${biobank.get('partner_charter_signed')?string("yes", "no")}</td>
                        </tr>
                        <tr>
                            <th scope="row">Biobank Description</th>
                            <#if biobank.get('description')??>
                                <td>${biobank.get('description')}</td>
                            </#if>
                        </tr>

                        <tr>
                            <th scope="row">Commercial collaborations</th>
                            <td>
                                <#if biobank.get('collaboration_commercial')??>
                                    ${biobank.get('collaboration_commercial')?string("yes", "no")}
                                    <#else>
                                        Not specified
                                </#if>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Non-profit collaborations</th>
                            <td>
                                <#if biobank.get('collaboration_non_for_profit')??>
                                    ${biobank.get('collaboration_non_for_profit')?string("yes", "no")}
                                    <#else>
                                        Not specified
                                </#if>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Biobank url</th>
                            <td>
                                <#if biobank.get('url')??>
                                    <a href="${biobank.get('url')}" target="_blank">${biobank.get('url')}</a>
                                </#if>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                <div class="col-md-4">
                    <h4>Main contact</h4>
                    <table class="table table-striped"
                    ">
                    <tbody>
                    ${biobankcontact()}
                    </tbody>
                    </table>
                </div>
                <div class="col-md-4">
                    <h4>Networks</h4>
                    <table class="table table-striped ">
                        <tbody>
                        <#list networks as network>
                            <tr>
                                <th scope="row">Name</th>
                                <td>
                                    ${network.get('name')}
                                    <#if network.get('acronym')??>
                                        ${network.get('acronym')}
                                    </#if>
                                    <#if network_has_next>,</#if>
                                </td>
                            </tr>
                        </#list>
                        </tbody>
                    </table>
                </div>
            </div>

        </#if>
        <!-- Collection details -->
        <div class="row">
            <div class="col-md-12">
                <hr></hr>
                <h3>${entity.get('name')}</h3>
                <small><strong>ID</strong>: ${entity.get('id')}</small>
                <br/><br/>
                <#if entity.get('description')??>
                    ${entity.get('description')}
                </#if>
            </div>
        </div>
        <hr></hr>


        <div class="row">
            <div class="col-md-4">
                <h4>Overview</h4>
                <table class="table table-striped ">
                    <tbody>
                    <tr>
                        <th scope="row">Type</th>
                        <td>
                            <#list entity.get('type') as type>
                                ${type.get('label')}
                                <#if type_has_next>,</#if>
                            </#list>
                        </td>
                    </tr>
                    <#if entity.get('size')?? && entity.get('size') gt 0>
                        <tr>
                            <th scope="row">Size</th>
                            <td>${entity.get('size')}</td>
                        </tr>
                        <#elseif entity.get('order_of_magnitude')??>
                            <tr>
                                <th scope="row">Size</th>
                                <td>${entity.get('order_of_magnitude').get('size')}</td>
                            </tr>
                    </#if>
                    <#if entity.get('sex')??>
                        <tr>
                            <th scope="row">Gender</th>
                            <td>
                                <#list entity.get('sex') as sex>
                                    ${sex.get('label')}
                                    <#if sex_has_next>,</#if>
                                </#list>
                            </td>
                        </tr>
                    </#if>
                    <#if entity.get('storage_temperatures')??>
                        <tr>
                            <th scope="row">Storage temperatures</th>
                            <td>
                                <#list entity.get('storage_temperatures') as temperatures>
                                    ${temperatures.get('label')}
                                    <#if temperatures_has_next>,</#if>
                                </#list>
                            </td>
                        </tr>
                    </#if>
                    <#if entity.get('materials')??>
                        <tr>
                            <th scope="row">Material types</th>
                            <td>
                                <#list entity.get('materials') as materials>
                                    <#if (materials.get('label'))??>
                                        ${materials.get('label')}
                                        <#if materials_has_next>,</#if>
                                    </#if>
                                </#list>
                            </td>
                        </tr>
                    </#if>
                    <tr>
                        <th scope="row">Available data</th>
                        <td>
                            <#list entity.get('data_categories') as categories>
                                ${categories.get('label')}
                                <#if categories_has_next>,</#if>
                            </#list>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Available diagnosis</th>
                        <td>
                            <#list entity.get('diagnosis_available') as diagnosis>
                                ${diagnosis.get('label')} (${diagnosis.get('id')})
                                <#if diagnosis_has_next>,</#if>
                            </#list>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>


            <div class="col-md-4">
                <h4>Main contact</h4>
                <table class="table table-striped ">
                    <tbody>
                    ${collectioncontact()}
                    </tbody>
                </table>
            </div>
            <div class="col-md-4">
                <h4>Networks</h4>
                <table class="table table-striped ">
                    <tbody>

                    <tr>
                        <th scope="row">Name</th>
                        <td>
                            <#list entity.get('network') as network>
                                ${network.get('name')}
                                <#if network.get('acronym')??>
                                    ${network.get('acronym')}
                                </#if>
                                <#if network_has_next>,</#if>
                            </#list>
                        </td>
                    </tr>

                    </tbody>

                </table>
            </div>
        </div>

        <hr></hr>

        <div class="row">
            <!-- Sample Access conditions -->
            <div class="col-md-4">
                <h4>Sample access conditions</h4>
                <table class="table table-striped ">
                    <tbody>
                    <tr>
                        <th scope="row">Sample Access Fee:</th>
                        <td>
                            <#if entity.get('sample_access_fee')??>
                                ${entity.get('sample_access_fee')?string("yes", "no")}
                                <#else>
                                    Not specified
                            </#if>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Sample Access on Joint Projects:</th>
                        <td>
                            <#if entity.get('sample_access_joint_project')??>
                                ${entity.get('sample_access_joint_project')?string("yes", "no")}
                                <#else>
                                    Not specified
                            </#if>
                        </td>
                    </tr>
                    <#if entity.get('sample_access_description')??>
                        <tr>
                            <th scope="row">Sample Access Rules:</th>
                            <td>
                                ${entity.get('sample_access_description')}
                            </td>
                        </tr>
                    </#if>
                    <#if entity.get('sample_access_uri')??>
                        <tr>
                            <th scope="row">Sample Access URI:</th>
                            <td>
                                <a href="${entity.get('sample_access_uri')}" target="_blank">${entity.get('sample_access_uri')}</a>
                            </td>
                        </tr>
                    </#if>
                    </tbody>
                </table>
            </div>
            <div class="col-md-4">
                <h4>Data access conditions</h4>
                <table class="table table-striped ">
                    <tbody>
                    <tr>
                        <th scope="row">Data Access Fee:</th>
                        <td>
                            <#if entity.get('data_access_fee')??>
                                ${entity.get('data_access_fee')?string("yes", "no")}
                                <#else>
                                    Not specified
                            </#if>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Data Access on Joint Projects:</th>
                        <td>
                            <#if entity.get('data_access_joint_project')??>
                                ${entity.get('data_access_joint_project')?string("yes", "no")}
                                <#else>
                                    Not specified
                            </#if>
                        </td>
                    </tr>
                    <#if entity.get('data_access_description')??>
                        <tr>
                            <th scope="row">Data Access Rules:</th>
                            <td>
                                ${entity.get('data_access_description')}
                            </td>
                        </tr>
                    </#if>
                    <#if entity.get('data_access_uri')??>
                        <tr>
                            <th scope="row">Data Access URI:</th>
                            <td>
                                <a href="${entity.get('data_access_uri')}" target="_blank">${entity.get('data_access_uri')}</a>
                            </td>
                        </tr>
                    </#if>
                    </tbody>
                </table>
            </div>
            <div class="col-md-4">
                <h4>Images access conditions</h4>
                <table class="table table-striped ">
                    <tbody>
                    <tr>
                        <th scope="row">Images Access Fee:</th>
                        <td>
                            <#if entity.get('image_access_fee')??>
                                ${entity.get('image_access_fee')?string("yes", "no")}
                                <#else>
                                    Not specified
                            </#if>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Images Access on Joint Projects:</th>
                        <td>
                            <#if entity.get('image_joint_projects')??>
                                ${entity.get('image_joint_projects')?string("yes", "no")}
                                <#else>
                                    Not specified
                            </#if>
                        </td>
                    </tr>
                    <#if entity.get('image_access_description')??>
                        <tr>
                            <th scope="row">Images Access Rules:</th>
                            <td>
                                ${entity.get('image_access_description')}
                            </td>
                        </tr>
                    </#if>
                    <#if entity.get('image_access_uri')??>
                        <tr>
                            <th scope="row">Images Access URI:</th>
                            <td>
                                <a href="${entity.get('image_access_uri')}" target="_blank">${entity.get('image_access_uri')}</a>
                            </td>
                        </tr>
                    </#if>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">close</button>
    </div>
</div>