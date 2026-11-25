package com.example.ticket_classifier.dto;

public class CreateTicketRequest {
    private String title;
    private String description;
    private String criticality;

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getCriticality() {
        return criticality;
    }

    public void setCriticality(String criticality) {
        this.criticality = criticality;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
