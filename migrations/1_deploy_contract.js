const CertificateContract = artifacts.require("CertificateStore");

module.exports = function(deployer) {
  deployer.deploy(CertificateContract);
};