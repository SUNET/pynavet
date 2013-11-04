<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output omit-xml-declaration="yes" indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <!-- Remove these tags that we know we don't need -->
    <xsl:template match="Riksnycklar|Arendeuppgift"/>

    <!-- Translate attributes to english -->
    <xsl:template match="Arendeuppgift/@andringstidpunkt">
        <xsl:attribute name="lastChange">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>

    <!-- Translate tags to english -->
    <xsl:template match="Navetavisering">
        <NavetNotifications><xsl:apply-templates select="@*|node()" /></NavetNotifications>
    </xsl:template>
    <xsl:template match="Folkbokforingsposter">
        <PopulationItems><xsl:apply-templates select="@*|node()" /></PopulationItems>
    </xsl:template>
    <xsl:template match="Folkbokforingspost">
        <PopulationItem><xsl:apply-templates select="@*|node()" /></PopulationItem>
    </xsl:template>
    <xsl:template match="Sekretessmarkering">
        <SecrecyMarking><xsl:apply-templates select="@*|node()" /></SecrecyMarking>
    </xsl:template>
    <xsl:template match="Personpost">
        <PersonItem><xsl:apply-templates select="@*|node()" /></PersonItem>
    </xsl:template>
    <xsl:template match="PersonNr">
        <NationalIdentityNumber><xsl:apply-templates select="@*|node()" /></NationalIdentityNumber>
    </xsl:template>
    <xsl:template match="Tilltalsnamnsmarkering">
        <GivenNameMarking><xsl:apply-templates select="@*|node()" /></GivenNameMarking>
    </xsl:template>
    <xsl:template match="Namn">
        <Name><xsl:apply-templates select="@*|node()" /></Name>
    </xsl:template>
    <xsl:template match="Fornamn">
        <GivenName><xsl:apply-templates select="@*|node()" /></GivenName>
    </xsl:template>
    <xsl:template match="Mellannamn">
        <MiddleName><xsl:apply-templates select="@*|node()" /></MiddleName>
    </xsl:template>
    <xsl:template match="Efternamn">
        <SurName><xsl:apply-templates select="@*|node()" /></SurName>
    </xsl:template>
    <xsl:template match="Adresser">
        <PostalAddresses><xsl:apply-templates select="@*|node()" /></PostalAddresses>
    </xsl:template>
    <xsl:template match="Utdelningsadress1">
        <Address1><xsl:apply-templates select="@*|node()" /></Address1>
    </xsl:template>
    <xsl:template match="Utdelningsadress2">
        <Address2><xsl:apply-templates select="@*|node()" /></Address2>
    </xsl:template>
    <xsl:template match="PostNr">
        <PostalCode><xsl:apply-templates select="@*|node()" /></PostalCode>
    </xsl:template>
    <xsl:template match="Postort">
        <City><xsl:apply-templates select="@*|node()" /></City>
    </xsl:template>
    <xsl:template match="Folkbokforingsadress">
        <OfficialAddress><xsl:apply-templates select="@*|node()" /></OfficialAddress>
    </xsl:template>
</xsl:stylesheet>
