"""
Email service for sending lead notifications to sales officers
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from loguru import logger
from app.config.settings import settings


class EmailService:
    """Send email notifications to sales officers"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM
    
    def send_lead_alert(self, officer_email: str, officer_name: str, lead_data: Dict) -> bool:
        """
        Send new lead alert email to sales officer
        
        Args:
            officer_email: Officer's email address
            officer_name: Officer's name
            lead_data: Lead information dictionary
        
        Returns:
            bool: True if sent successfully
        """
        try:
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🔔 New Lead: {lead_data['company_name']} - {lead_data['intent_strength'].upper()} Priority"
            msg['From'] = self.from_email
            msg['To'] = officer_email
            
            # Create HTML content
            html_content = self._create_lead_email_html(officer_name, lead_data)
            
            # Attach HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Lead alert email sent to {officer_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {officer_email}: {e}")
            return False
    
    def _create_lead_email_html(self, officer_name: str, lead_data: Dict) -> str:
        """Create professional HTML email template"""
        
        # Product recommendations HTML
        products_html = ""
        for product in lead_data.get('recommended_products', []):
            confidence_percent = int(product['confidence'] * 100)
            products_html += f"""
            <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #003DA5;">
                <div style="font-weight: bold; color: #003DA5; margin-bottom: 4px;">
                    {product['product']} 
                    <span style="background: #16A34A; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 8px;">
                        {confidence_percent}% Match
                    </span>
                </div>
                <div style="font-size: 13px; color: #64748b;">
                    {product['reason']}
                </div>
            </div>
            """
        
        # Keywords HTML
        keywords_html = ""
        for keyword in lead_data.get('detected_keywords', []):
            keywords_html += f'<span style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 12px; margin: 4px; display: inline-block; font-size: 12px;">{keyword}</span>'
        
        # Intent badge color
        intent_colors = {
            "high": "#16A34A",
            "medium": "#F59E0B",
            "low": "#64748b"
        }
        intent_color = intent_colors.get(lead_data.get('intent_strength', 'low'), "#64748b")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color: #f8fafc;">
            <div style="max-width: 600px; margin: 0 auto; background: white;">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #003DA5 0%, #0052cc 100%); padding: 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
                        🎯 New Lead Alert
                    </h1>
                    <p style="color: #e0f2fe; margin: 8px 0 0 0; font-size: 14px;">
                        HPCL Direct Sales Lead Intelligence
                    </p>
                </div>
                
                <!-- Content -->
                <div style="padding: 30px;">
                    
                    <!-- Greeting -->
                    <p style="font-size: 16px; color: #1e293b; margin: 0 0 20px 0;">
                        Hello <strong>{officer_name}</strong>,
                    </p>
                    
                    <p style="font-size: 14px; color: #475569; margin: 0 0 24px 0;">
                        A new lead has been assigned to you based on your territory. Here are the details:
                    </p>
                    
                    <!-- Lead Score Banner -->
                    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 20px; border-radius: 8px; margin-bottom: 24px; text-align: center;">
                        <div style="font-size: 14px; color: #64748b; margin-bottom: 4px;">Lead Score</div>
                        <div style="font-size: 36px; font-weight: bold; color: #003DA5;">{lead_data.get('lead_score', 0)}/100</div>
                        <div style="margin-top: 8px;">
                            <span style="background: {intent_color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 600; text-transform: uppercase;">
                                {lead_data.get('intent_strength', 'Low')} Priority
                            </span>
                        </div>
                    </div>
                    
                    <!-- Company Info -->
                    <div style="border: 2px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
                        <h2 style="margin: 0 0 16px 0; color: #003DA5; font-size: 20px;">
                            {lead_data.get('company_name', 'Unknown Company')}
                        </h2>
                        
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; color: #64748b; font-size: 13px; width: 120px;">Industry:</td>
                                <td style="padding: 8px 0; color: #1e293b; font-size: 14px; font-weight: 500;">{lead_data.get('industry', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #64748b; font-size: 13px;">Location:</td>
                                <td style="padding: 8px 0; color: #1e293b; font-size: 14px; font-weight: 500;">{lead_data.get('location', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #64748b; font-size: 13px;">Signal Type:</td>
                                <td style="padding: 8px 0; color: #1e293b; font-size: 14px; font-weight: 500;">{lead_data.get('signal_type', 'N/A')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <!-- Recommended Products -->
                    <div style="margin-bottom: 24px;">
                        <h3 style="color: #1e293b; font-size: 16px; margin: 0 0 12px 0;">
                            📦 Recommended Products
                        </h3>
                        {products_html}
                    </div>
                    
                    <!-- Signal Context -->
                    <div style="background: #fefce8; border-left: 4px solid #F59E0B; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
                        <h3 style="color: #854d0e; font-size: 14px; margin: 0 0 8px 0; font-weight: 600;">
                            💡 Signal Context
                        </h3>
                        <p style="color: #713f12; font-size: 13px; margin: 0; line-height: 1.6;">
                            {lead_data.get('signal_text', 'No signal text available')[:300]}...
                        </p>
                    </div>
                    
                    <!-- Detected Keywords -->
                    <div style="margin-bottom: 24px;">
                        <h3 style="color: #1e293b; font-size: 14px; margin: 0 0 12px 0;">
                            🔍 Detected Keywords
                        </h3>
                        <div style="line-height: 2;">
                            {keywords_html}
                        </div>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div style="text-align: center; margin: 32px 0;">
                        <a href="{lead_data.get('dossier_url', '#')}" 
                           style="background: #003DA5; color: white; padding: 14px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block; margin: 8px;">
                            📄 View Full Dossier
                        </a>
                        <a href="tel:{lead_data.get('contact_phone', '')}" 
                           style="background: #16A34A; color: white; padding: 14px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block; margin: 8px;">
                            📞 Call Now
                        </a>
                    </div>
                    
                    <!-- Next Action -->
                    <div style="background: #f1f5f9; padding: 16px; border-radius: 6px; margin-top: 24px;">
                        <h3 style="color: #1e293b; font-size: 14px; margin: 0 0 8px 0;">
                            ⚡ Suggested Next Action
                        </h3>
                        <p style="color: #475569; font-size: 13px; margin: 0;">
                            {lead_data.get('next_action', 'Review the dossier and contact the company to discuss their requirements.')}
                        </p>
                    </div>
                    
                </div>
                
                <!-- Footer -->
                <div style="background: #f8fafc; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #64748b; font-size: 12px; margin: 0;">
                        This is an automated lead alert from HPCL Lead Intelligence System<br>
                        For support, contact your DSRO office
                    </p>
                    <div style="margin-top: 12px;">
                        <img src="https://www.hindustanpetroleum.com/documents/20121/22295/hp_logo.png" 
                             alt="HPCL Logo" 
                             style="height: 40px;">
                    </div>
                </div>
                
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_daily_digest(self, officer_email: str, officer_name: str, leads: List[Dict]) -> bool:
        """Send daily digest of new leads"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Daily Lead Digest - {len(leads)} New Leads"
            msg['From'] = self.from_email
            msg['To'] = officer_email
            
            # Create digest HTML
            html_content = self._create_digest_html(officer_name, leads)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Daily digest sent to {officer_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send digest to {officer_email}: {e}")
            return False
    
    def _create_digest_html(self, officer_name: str, leads: List[Dict]) -> str:
        """Create daily digest HTML"""
        # Simple digest - you can enhance this
        leads_html = ""
        for lead in leads:
            leads_html += f"""
            <div style="border-bottom: 1px solid #e2e8f0; padding: 12px 0;">
                <strong>{lead['company_name']}</strong> - Score: {lead['lead_score']}/100
            </div>
            """
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Daily Lead Digest</h2>
            <p>Hello {officer_name},</p>
            <p>You have {len(leads)} new leads today:</p>
            {leads_html}
        </body>
        </html>
        """