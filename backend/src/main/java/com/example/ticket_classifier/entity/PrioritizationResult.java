package com.example.ticket_classifier.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "prioritization_results")
public class PrioritizationResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne // Так как у одного тикета может быть только один такой детальный результат анализа
    @JoinColumn(name = "ticket_id", nullable = false) // Чтобы указать колонку внешнего ключа
    private Ticket ticket;

    private String sentiment; // тональность
    private Integer priority;
    private Double confidence; //уверенность модели в своем ответе

    public PrioritizationResult() {
    }

    public Long getId() {
        return id;
    }

    public Ticket getTicket() {
        return ticket;
    }

    public String getSentiment() {
        return sentiment;
    }

    public Integer getPriority() {
        return priority;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setTicket(Ticket ticket) {
        this.ticket = ticket;
    }

    public void setSentiment(String sentiment) {
        this.sentiment = sentiment;
    }

    public void setPriority(Integer priority) {
        this.priority = priority;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }
}
