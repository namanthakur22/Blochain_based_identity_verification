// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.4.22 <0.9.0;

contract CertificateStore {
    struct Certificate {
        string name;
        string organization;
        string certificateFor;
        uint256 assignedDate;
        uint256 expireDate;
        string email;
        string certificateId;
    }

    Certificate[] public certificates;

    function addCertificate(
        string memory _name,
        string memory _organization,
        string memory _certificateFor,
        uint256 _assignedDate,
        uint256 _expireDate,
        string memory _email,
        string memory _certificateId
    ) public {
        certificates.push(Certificate(_name, _organization, _certificateFor, _assignedDate, _expireDate, _email, _certificateId));
    }

    function getCertificateCount() public view returns (uint256) {
        return certificates.length;
    }

        function getCertificateIndex(string memory _certificateId) public view returns (uint256) {
        for (uint256 i = 0; i < certificates.length; i++) {
            if (keccak256(bytes(certificates[i].certificateId)) == keccak256(bytes(_certificateId))) {
                return i + 1; // Adding 1 to make the index 1-based instead of 0-based
            }
        }
        return 0; // Return 0 if the certificate is not found
    }

    function getCertificateData(string memory _certificateId) public view returns (
        string memory name,
        string memory organization,
        string memory certificateFor,
        uint256 assignedDate,
        uint256 expireDate,
        string memory email,
        string memory certificateId
    ) {
        uint256 index = getCertificateIndex(_certificateId);
        require(index > 0, "Certificate not found");
        
        Certificate memory certificate = certificates[index - 1]; // Subtract 1 to convert 1-based index to 0-based index
        return (
            certificate.name,
            certificate.organization,
            certificate.certificateFor,
            certificate.assignedDate,
            certificate.expireDate,
            certificate.email,
            certificate.certificateId
        );
    }
}